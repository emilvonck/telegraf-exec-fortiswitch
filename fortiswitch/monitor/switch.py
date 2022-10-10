import json

from requests.sessions import Session

from fortiswitch.core import get_req
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "api/v2/monitor/switch"
HEADERS = {"Accept": "application/json"}


def get_port_state(session: Session):
    endpoint = "port"
    url = f"https://{session.host}:{session.port}/{BASE_URL}/{endpoint}"

    response_data = get_req(session=session, url=url).json()

    return json.dumps(response_data)


def get_poe_status(session: Session):
    endpoint = "poe-status"
    url = f"https://{session.host}:{session.port}/{BASE_URL}/{endpoint}"

    response_data = get_req(session=session, url=url).json()

    return json.dumps(response_data)
