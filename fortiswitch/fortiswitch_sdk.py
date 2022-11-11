# noqa: D100
from sys import version as python_version

import requests
import urllib3

from fortiswitch.utils import LogHandler

logging = LogHandler(__name__)


class FortiSwitch:
    """Class for interacting with the FortiSwitchOS API."""

    def __init__(self, host: str, username: str, password: str, verify: bool = True):
        """Initializor for the class.

        Args:
            host (str): Host for the API, IP or DNSname.
            username (str): Username.
            password (str): Password.
            verify (bool, optional): Whether to verify SSL certificates or not. Defaults to True.
        """
        self.host = host
        self.username = username
        self.password = password
        self._verify = verify
        self.session = requests.Session()

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"Python {python_version.split(' ', maxsplit=1)[0]}",
        }

        self._monitor_base_url = "api/v2/monitor"

    @property
    def verify(self):
        # noqa: D102
        return self._verify

    @verify.setter
    def verify(self, value: bool):
        # noqa: D102
        if not isinstance(value, bool):
            raise TypeError(f"invalid type for '{value}' must be of type {type(True)}")
        else:
            self._verify = value

    @property
    def hostname(self):
        # noqa: D102
        return self.system_status["hostname"]

    @property
    def serial_number(self):
        # noqa: D102
        return self.system_status["serial_number"]

    @property
    def system_status(self):
        # noqa: D102
        return self.extractors["system_status"]

    @property
    def extractors(self):
        # noqa: D102
        extractors = {"system_status": self._get_system_status()}

        return extractors

    def _login(self):
        base_url = "login"
        url = f"https://{self.host}/{base_url}"

        data = {
            "username": self.username,
            "password": self.password,
        }

        self._req(url=url, method="post", body=data)

    def _logout(self):
        base_url = "logout"
        url = f"https://{self.host}/{base_url}"

        self._req(url=url, method="post")

    def _req(self, url, method="get", params=None, body=None):

        logging_dict = {
            "message_type": f"http {method}",
            "url": url,
        }

        if not self.verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        response = self.session.request(
            url=url, data=body, params=params, method=method, verify=self.verify
        )

        if response:
            level = 20
            logging_dict.update(
                {
                    "message": response.reason,
                    "status_code": response.status_code,
                    "level": level,
                    "response_url": response.url,
                }
            )

        else:
            level = 30
            logging_dict.update(
                {
                    "message": response.reason,
                    "status_code": response.status_code,
                    "level": level,
                    "response_url": response.url,
                }
            )

        logging.format_logs(**logging_dict)

        return response

    def _get_system_status(self) -> dict:
        self._login()
        base_url = "system/status"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self._req(url=url, method="get")
        self._logout()

        return result.json()["results"]
