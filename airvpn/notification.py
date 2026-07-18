from airvpn.network import AirSession

def send_notification(session: AirSession, subject: str, body: str):
    """Send a message to yourself.

    Args:
        session: The active AirSession used to make the API request.
        subject: The notification's subject line.
        body: The notification's message content.

    Returns:
        True if the notification was sent successfully, False otherwise.

    Access type:
        User-specific, API KEY required.
    """
    response = session.get("notification", params={"subject": subject, "body": body})

    return response.json().get("result") == "ok"