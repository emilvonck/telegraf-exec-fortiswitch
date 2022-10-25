"""Functions for interacting with FortiSwitchOS API."""
import json
import sys

from requests.sessions import Session

from fortiswitch.core import req
from fortiswitch.logging import LogHandler

BASE_URL = "api/v2/monitor/switch"
HEADERS = {"Accept": "application/json"}

logging = LogHandler(__name__)


def get_port_state(session: Session):
    """Get switch port state.

    Args:
        session (Session): requests.Session()

    Returns:
        _type_: str
    """
    endpoint = "port"
    url = f"https://{session.host}:{session.port}/{BASE_URL}/{endpoint}"

    return_data = []

    try:
        response_data = req(session=session, url=url).json()
        for _, interface_property in response_data["results"].items():
            return_data.append(interface_property)
        log_dict = {
            "level": 20,
            "message_type": "Parse",
            "message": f"Successfully parsed {len(return_data)} interfaces {url}",
        }
        logging.format_logs(**log_dict)
        return json.dumps(return_data)

    except KeyError as err:
        logging.format_logs(level=40, message_type="KeyError", message=f"{err}")
        sys.exit(1)


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
