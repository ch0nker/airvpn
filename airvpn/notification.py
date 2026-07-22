from airvpn.network import AirSession

def send_notification(session: AirSession, subject: str, body: str):
    """Send a message to yourself.

    Args:
        session: The active AirSession used to make the API request.
        subject: The notification's subject line.
        body: The notification's message content.

    Raises:
        APIError: If it fails to send the message.
        RateLimited: If too many requests go through.

    Access type:
        User-specific, API KEY required.
    """
    session.service_request("post", "notification", data={"subject": subject, "body": body})