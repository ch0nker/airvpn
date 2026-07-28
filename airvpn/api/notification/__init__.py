from airvpn.api.network import AirSession

class Notification:
    """Service for handling notifications.

    Access type:
        User-specific, API KEY required.

    Choose in the notifications options (https://airvpn.org/notifications/options/), 
    under Air -> API, if you want to see it in the web site and/or in an e-mail.
    """

    __KEY_NEEDED__ = True

    def __init__(self, session: AirSession):
        self._session = session

    def send(self, subject: str, body: str):
        """Send a message to yourself.

        Args:
            subject: The notification's subject line.
            body: The notification's message content.

        Raises:
            APIError: If it fails to send the message.
            RateLimited: If too many requests go through.

        """
        self._session.service_request("post", "notification", data={"subject": subject, "body": body})