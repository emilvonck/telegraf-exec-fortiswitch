"""Functions for requests."""
import sys

import requests
from requests.sessions import Session

from fortiswitch.core.session import logout
from fortiswitch.logging import LogHandler

logging = LogHandler(__name__)

HEADERS = {"Accept": "application/json"}


def req(session: Session, url: str):
    """Standardized function for requests.

    Args:
        session (Session): Session object.
        url (str): complete url for request.

    Returns:
        _type_: requests.Response()
    """
    try:
        response = session.get(url=url, headers=HEADERS, verify=session.ignore_ssl)
        """ log_dict = {
            "level": 20,
            "message_type": "HTTPSuccess",
            "message": url,
            "http_response_code": response.status_code,
        }
        logging.format_logs(**log_dict) """
        return response
    except requests.exceptions.HTTPError as err:
        logging.format_logs(level=40, message_type="HTTPError", message=err)
        sys.exit(1)

    finally:
        logout(session)
