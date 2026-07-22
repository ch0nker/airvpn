from airvpn.network import AirSession


def disconnect(session: AirSession,
               server_name: str = None,
               device_id: str = None):
    """Requests a disconnection. If none of the filter parameters is specified, disconnect all sessions of the user.

    Args:
        session: The active AirSession used to make the API request.
        server_name: Name of the server to disconnect from. Ignored if
            server is provided.
        device_id: ID of the device to disconnect. Ignored if device
            is provided.

    Returns:
        The number of sessions that were disconnected.
    
    Raises:
        APIError: If it fails to disconnect.
        RateLimited: If too many requests go through.

    Access type:
        User-specific, API KEY required.
    """

    json = session.service_request("post", "disconnect", data={
        "server": server_name,
        "device": device_id
    })

    return json.get("sessions_disconnected", 0)