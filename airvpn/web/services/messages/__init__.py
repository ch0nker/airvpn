from __future__ import annotations

from airvpn.web.user import WebUser
from airvpn.web.network import WebSession
from airvpn.exceptions import ValidationError

from bs4 import BeautifulSoup
from datetime import datetime, timezone
from requests.exceptions import JSONDecodeError

class Message:
    """
    Represents a single message within a conversation.

    Attributes:
        conversation (Conversation): The conversation this message belongs to.
        session (WebSession): The active web session used for requests.
        user (WebUser): The user who sent the message.
        content (str): The stripped content of the message.
        timestamp (datetime): UTC datetime of when the message was sent.
        id (int): The unique ID of the message (comment ID).
    """

    def __init__(self, session: WebSession, conversation: Conversation, user: WebUser, content: str, id: int, timestamp: int):
        self.conversation = conversation
        self.session = session
        self.user = user
        self.content = content.strip()
        self.timestamp = datetime.fromtimestamp(timestamp, timezone.utc)
        self.id = id

    def edit(self, content: str):
        """
        Edit this message's content.

        Args:
            content (str): The new content to replace the existing message body.

        Raises:
            ValidationError: If the current user is not the owner of the message/conversation.
        """
        if self.user.id != self.conversation.owner_id:
            raise ValidationError("You cannot edit a message you didn't send.")

        self.session.request("post", f"https://airvpn.org/messenger/{self.conversation.id}/", params={
            "do": "editComment",
            "comment": self.id
        }, data={
            "form_submitted": 1,
            "csrfKey": self.session.csrf,
            "comment_value": content
        })

        self.content = content

class Conversation:
    """
    Represents a messenger conversation (thread) with one or more participants.

    Attributes:
        owner_id (int): The user ID of the conversation owner (the authenticated user).
        session (WebSession): The active web session used for requests.
        title (str): The conversation's title/subject.
        body (str): A snippet/preview of the conversation's body content.
        id (int): The unique ID of the conversation.
        messages (list[Message]): The messages belonging to this conversation, fetched on first access.
    """

    def __init__(self, session: WebSession, owner_id: int, title: str, body: str, id: int):
        self.owner_id = owner_id
        self.session = session
        self.title = title
        self.body = body
        self.id = id
        self._messages: list[Message] = None

    @property
    def messages(self):
        if self._messages is None:
            self.update()

        return self._messages

    def update(self, page = 1):
        """
        Fetch and parse the conversation's messages from the given page, replacing
        the cached message list.

        Args:
            page (int, optional): The page number of messages to retrieve. Defaults to 1.
        """
        response = self.session.request("get", f"https://airvpn.org/messenger/{self.id}/", params={"page": page})
        soup = BeautifulSoup(response.text, "html.parser")

        comments = soup.find_all("article", {"class": "ipsComment"})

        self._messages = []

        for comment in comments:
            content = comment.find("div", {"class": "ipsComment_content"})
            header = content.find("div", {"class": "ipsComment_header"})
            user_elm = header.find("a", {"class": "ipsType_break"})

            username = user_elm.text
            url = user_elm.get("href")
            id = int(url.split("-")[0].split("/")[-1])

            img = header.find("img", {"alt": username})

            user = WebUser(self.session, name=username, id=id, image=img)

            timestamp_elm = header.find("span", {"data-ui-type": "datetime"})
            timestamp = int(timestamp_elm.get("data-unix"))

            body_elm = content.find("div", {"data-role": "commentContent"})

            id = int(content.get("data-commentid"))

            message = Message(self.session, self.owner_id, user, body_elm.decode_contents(), id, timestamp)

            self._messages.append(message)

class InboxManager:
    """
    Manages the authenticated user's messenger inbox and conversations.

    Attributes:
        session (WebSession): The active web session used for requests.
        owner_id (int): The user ID of the authenticated user (inbox owner).
        conversations (list[Conversation]): The list of conversations in the inbox.
    """

    def __init__(self, session: WebSession, owner_id: int):
        self.session = session
        self.owner_id = owner_id
        self.conversations: list[Conversation] = []
        self.update()

    def update(self):
        """
        Fetch and parse the list of conversations from the messenger inbox page,
        appending any found conversations to `self.conversations`.
        """
        response = self.session.request("get", "https://airvpn.org/messenger/")
        soup = BeautifulSoup(response.text, "html.parser")

        message_list = soup.find("div", id="elMessageList")

        conversations = message_list.find_all("li", {"class": "cMessage"})

        for conversation_elm in conversations:
            id = conversation_elm.get("data-messageid")
            title = conversation_elm.find("a", {"class": "cMessageTitle"}).text
            body = conversation_elm.find("div", {"class": "ipsMessageRow"}).text

            self.conversations.append(Conversation(self.session, self.owner_id, title, body, int(id)))

    def start_conversation(self, username: str, subject: str, body: str) -> Conversation:
        """
        Create a conversation with a user.

        Args:
            username (str): The username of the recipient.
            subject (str): The subject of the message.
            body (str): The body content of the message.

        Returns:
            Conversation | None: returns the created conversation.
        """
        response = self.session.request("post", "https://airvpn.org/messenger/compose/", headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }, data = {
                "csrfKey": self.session.csrf,
                "form_submitted": 1,
                "messenger_to_original": "",
                "messenger_to": username,
                "messenger_title": subject,
                "messenger_content": body
        })

        try:
            data = response.json()
            redirect_url = data.get("redirect")
            conversation_id = redirect_url.rstrip("/").split("/")[-1]

            conversation = Conversation(self.session, self.owner_id, subject, body, int(conversation_id))
            self.conversations.append(conversation)

            return conversation
        except JSONDecodeError:
            return None