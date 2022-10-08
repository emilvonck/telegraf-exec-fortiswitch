from typing import Any

from requests.sessions import Session

from fortiswitch.core import logout

HEADERS = {"Accept": "application/json"}


def get_req(session: Session, url: str):
    response = session.get(url=url, headers=HEADERS, verify=session.ssl_verify)
    logout(session)

    return response
