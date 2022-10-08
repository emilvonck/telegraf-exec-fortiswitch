from requests.sessions import Session


def login(
    username: str,
    password: str,
    host: str,
    ssl_verify: bool = True,
    endpoint: str = "login",
    port: bool = 443,
    **kwargs,
) -> Session:
    """Login function.

    Args:
        username (str): username for device.
        password (str): password for device.
        host (str): device to interface with.
        ssl_verify (bool, optional): Whether to verify SSL or not. Defaults to True.
        endpoint (str, optional): login endpoint. Defaults to "/login".

    Returns:
        Session: A Requests session. Provides cookie persistence.
    """
    data = {
        "username": username,
        "password": password,
    }
    url = f"https://{host}:{port}/{endpoint}"
    session = Session()
    response = session.post(url, data=data, verify=ssl_verify)

    response.raise_for_status()

    session.host = host
    session.port = port
    session.ssl_verify = ssl_verify

    return session


def logout(session: Session, endpoint: str = "/logout") -> None:
    """Logout function.

    Args:
        session (Session): Session to be logged out.
        endpoint (str, optional): endpoint for logout. Defaults to "/logout".
    """
    session.post(url=f"https://{session.host}:{session.port}/{endpoint}")
