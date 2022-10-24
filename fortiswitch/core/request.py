"""Functions for requests."""
from requests.sessions import Session

from fortiswitch.core import logout

HEADERS = {"Accept": "application/json"}


def req(session: Session, url: str):
    """Standardized function for requests.

    Args:
        session (Session): Session object.
        url (str): complete url for request.

    Returns:
        _type_: requests.Response()
    """
    response = session.get(url=url, headers=HEADERS, verify=session.ignore_ssl)
    logout(session)

    return response
