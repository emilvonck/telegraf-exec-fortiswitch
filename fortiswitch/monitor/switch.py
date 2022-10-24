"""Functions for interacting with FortiSwitchOS API."""
import json

import urllib3
from requests.sessions import Session

from fortiswitch.core import req

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "api/v2/monitor/switch"
HEADERS = {"Accept": "application/json"}


def get_port_state(session: Session):
    """Get switch port state.

    Args:
        session (Session): requests.Session()

    Returns:
        _type_: str
    """
    endpoint = "port"
    url = f"https://{session.host}:{session.port}/{BASE_URL}/{endpoint}"

    response_data = req(session=session, url=url).json()

    return json.dumps(response_data)


def get_poe_status(session: Session):
    """Get switch poe-status.

    Args:
        session (Session): requests.Session()

    Returns:
        _type_: str
    """
    endpoint = "poe-status"
    url = f"https://{session.host}:{session.port}/{BASE_URL}/{endpoint}"

    response_data = req(session=session, url=url).json()

    return json.dumps(response_data)
