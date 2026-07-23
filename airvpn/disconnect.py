from airvpn.network import AirSession


def disconnect(session: AirSession,
               server_name: str = None,
               device: str = None):
    """Requests a disconnection. If none of the filter parameters is specified, disconnect all sessions of the user.

    Args:
        session: The active AirSession used to make the API request.
        server_name: Name of the server to disconnect from.
        device: ID/name of the device to disconnect.

    Returns:
        The number of sessions that were disconnected.
    
    Raises:
        APIError: If it fails to disconnect.
        RateLimited: If too many requests go through.

    Access type:
        User-specific, API KEY required.
    """

    # This doesn't seem to disconnect, even when I do it through the api page??
    # or at least the sessions page doesn't update.

    json = session.service_request("get", "disconnect", data={
        "server": server_name,
        "device": device
    })

    return json.get("sessions_disconnected", 0)