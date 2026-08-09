from __future__ import annotations

from typing import Optional, TypeVar, Generic, Iterator, Never
from abc import ABC, abstractmethod

from airvpn.web.network import WebSession
from airvpn.web.user import WebUser

from bs4 import BeautifulSoup

import json

class Comment:
    """A single reply/post within a forum topic.

    Attributes:
        user (WebUser): The author of the comment.
        id (int): The comment's unique content-comment id.
        content (str): The comment's HTML content.
    """

    def __init__(self, user: WebUser, id: int, content: str):
        self.user = user
        self.id = id
        self.content = content

T = TypeVar("T")

class BasePagination(ABC, Generic[T]):
    def __init__(self, url: str):
        self.url = url.rstrip('/')
        self.pages: dict[int, list[T]] = {}

    @abstractmethod
    def update(self, page: int) -> Never:
        ...

    def get_url(self, page: int):
        return f"{self.url}/page/{page}/"

    def __iter__(self) -> Iterator[list[T]]:
        yield from self.pages.values()

    def __getitem__(self, index: int) -> list[T]:
        if index in self.pages:
            return self.pages[index]

        self.update(index + 1)

        return self.pages[index]

class TopicPagination(BasePagination[Comment]):
    """Lazily fetches and caches pages of comments for a forum topic.

    Attributes:
        session (WebSession): The session used to fetch pages.
        max_page (int): The total number of pages available for this topic.
        url (str): The topic's base URL (inherited from BasePagination).
        pages (dict[int, list[Comment]]): Cache of fetched pages, keyed by 0-indexed page number (inherited from BasePagination).
    """

    def __init__(self, session: WebSession, url: str, max_page: int):
        """Initialize pagination bound to a topic URL and its known max page count."""
        super().__init__(url)
        self.session = session
        self.max_page = max_page

    def update(self, page: int = 1):
        """Fetch `page` (1-indexed) from the topic and store parsed comments as self.pages[page - 1].

        Raises IndexError if `page` is at or beyond `self.max_page`.
        """
        if page >= self.max_page:
            raise IndexError(f"Page {page} exceeds max of {self.max_page}.")

        response = self.session.request("get", self.get_url(page))
        soup = BeautifulSoup(response.text, "html.parser")

        post_feed = soup.find("div", id="elPostFeed")

        comments = []
        for article in post_feed.find_all("article"):
            quote_elm = article.find("div", {"class": "ipsComment_content"})
            quote_data = json.loads(quote_elm.get("data-quotedata"))

            user = WebUser(self.session, name=quote_data.get("username"), id=quote_data.get("userid"))
            comment_id = quote_data.get("contentcommentid")

            content_elm = article.find("div", {"data-role": "commentContent"})

            comments.append(Comment(user, comment_id, content_elm.decode_contents()))

        self.pages[page - 1] = comments

class Topic:
    """A single forum topic/thread, with lazily-paginated access to its comments.

    Attributes:
        session (WebSession): The session used to fetch related resources.
        user (WebUser): The user who started the topic.
        id (int): The topic's unique id.
        url (str): The topic's URL.
        title (str): The topic's title.
        reply_count (int): The number of replies in the topic.
        views (int): The number of views the topic has received.
        max_page (int): The total number of comment pages in the topic.
        pages (TopicPagination): Lazily-loaded, paginated access to the topic's comments.
    """

    def __init__(self, 
                 session: WebSession, 
                 user: WebUser, 
                 title: str, 
                 id: int,
                 url: str,
                 reply_count: int, 
                 views: int, 
                 max_page: int):
        self.session = session
        self.user = user
        self.id = id
        self.url = url
        self.title = title
        self.reply_count = reply_count
        self.views = views
        self.max_page = max_page
        self.pages = TopicPagination(self.session, self.url, self.max_page)

class ForumPagination(BasePagination[Topic]):
    """Lazily fetches and caches pages of topics for a forum.

    Attributes:
        session (WebSession): The session used to fetch pages.
        url (str): The forum's base URL (inherited from BasePagination).
        pages (dict[int, list[Topic]]): Cache of fetched pages, keyed by 0-indexed page number (inherited from BasePagination).
    """

    def __init__(self, session: WebSession, url: str):
        """Initialize pagination bound to a forum URL."""
        super().__init__(url)
        self.session = session
    
    def update(self, page: int = 1):
        """Fetch `page` (1-indexed) from the forum and store parsed topics as self.pages[page - 1].

        Raises IndexError if `page` doesn't exist (the forum redirects back to its base URL).
        """
        response = self.session.request("get", self.get_url(page))

        if response.url == self.url and page != 1:
            raise IndexError(f"Page {page} doesn't exist.")
        
        soup = BeautifulSoup(response.text, "html.parser")

        topic_table = soup.find("ol", {"class": "cForumTopicTable"})
        topics = []
        for topic_elm in topic_table.find_all("li", {"data-rowid": True}):
            main = topic_elm.find("div", {"class": "ipsDataItem_main"})

            title_elm = main.find("a", {"title": True, "data-ipshover-target": True})
            title = title_elm.get("title").strip()
            url = title_elm.get("href")
            topic_id = int(url.rstrip("/").split("/")[-1].split("-")[0])

            max_page = 1
            pagination_elm = main.find("ul", {"class": "ipsPagination"})
            if pagination_elm is not None:
                last_page = pagination_elm.find_all("a")[-1]
                max_page = int(last_page.text.strip())

            meta_elm = main.find("div", {"class": "ipsDataItem_meta"})
            user_elm = meta_elm.find("a")

            username = user_elm.text
            id = user_elm.get("href").rstrip("/").split("/")[-1].split("-")[0]

            user = WebUser(self.session, name=username, id=int(id))

            views = 0
            reply_count = 0

            stats = topic_elm.find("ul", {"class": "ipsDataItem_stats"})
            for item in stats.find_all("li"):
                number, type = item.find_all("span")

                number = int(number.text)
                type = type.text.strip()

                if type == "replies":
                    reply_count = number
                elif type == "views":
                    views = number

            topics.append(Topic(self.session, user, title, topic_id, url, reply_count, views, max_page))

        self.pages[page - 1] = topics

class Forum:
    """A forum section, with lazily-paginated access to its topics and any sub-forums.

    Attributes:
        session (WebSession): The session used to fetch related resources.
        title (str): The forum's title.
        url (str): The forum's URL.
        description (Optional[str]): The forum's description, if any.
        sub_forums (list[Forum]): Any child forums nested under this one.
        pages (ForumPagination): Lazily-loaded, paginated access to the forum's topics.
    """

    def __init__(self,
                 session: WebSession,
                 title: str,
                 url: str,
                 description: Optional[str] = None,
                 sub_forums: Optional[list[Forum]] = None):
        self.session = session
        self.title = title
        self.url = url
        self.description = description
        self.sub_forums = sub_forums or []
        self.pages = ForumPagination(self.session, self.url)

class Category:
    """A top-level grouping of forums, fetched and cached on first access.

    Attributes:
        session (WebSession): The session used to fetch related resources.
        title (str): The category's title.
        url (str): The category's URL.
        forums (list[Forum]): The forums in this category, fetched and cached lazily on first access.
    """

    def __init__(self, session: WebSession, title: str, url: str):
        self.session = session
        self.title = title
        self._forums = []
        self.url = url

    @property
    def forums(self) -> list[Forum]:
        """The forums in this category, fetching them on first access if not already loaded."""
        if len(self._forums) == 0:
            self.update()

        return self._forums

    def update(self, forums: Optional[list] = None):
        """Parse and (re)populate self.forums.

        If `forums` (a list of forum <li> elements) isn't provided, fetches and parses
        the category page first.
        """
        self._forums = []

        if forums is None:
            response = self.session.request("get", self.url)
            soup = BeautifulSoup(response.text, "html.parser")

            forums = soup.find_all("li", {"class": "cForumRow", "data-forumid": True})

        for forum_elm in forums:
            main = forum_elm.find("div", {"class": "ipsDataItem_main"})
            title_a = main.find("h4", {"class": "ipsDataItem_title"}).find("a")
            meta_div = main.find("div", {"class": "ipsDataItem_meta"})
            sublist_ul = main.find("ul", {"class": "ipsDataItem_subList"})

            sub_forums = []
            if sublist_ul:
                for sub_elm in sublist_ul.find_all("a"):
                    sub_title = sub_elm.text.strip()
                    sub_url = sub_elm.get("href")

                    sub_forums.append(Forum(self.session, sub_title, sub_url))

            title = title_a.text.strip()
            url = title_a.get("href")
            description = meta_div.text.strip()

            self._forums.append(Forum(self.session, title, url, description, sub_forums))