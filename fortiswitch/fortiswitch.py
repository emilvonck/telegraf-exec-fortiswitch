# noqa: D100
from sys import version as python_version

import requests
import urllib3


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
        self.verify = verify
        self.session = requests.Session()

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"Python {python_version.split(' ', maxsplit=1)[0]}",
        }

        self._monitor_base_url = "api/v2/monitor"
        self._system_status = self._get_system_status()

    @property
    def hostname(self):
        # noqa: D102
        return self.extractors["hostname"]

    @property
    def serial_number(self):
        # noqa: D102
        return self.extractors["serial_number"]

    @property
    def extractors(self):
        # noqa: D102
        extractors = {
            "hostname": self._system_status["hostname"],
            "serial_number": self._system_status["serial_number"],
        }

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

        self._req(url=url, method="post", raise_for_status=False)

    def _req(
        self, url, method="get", params=None, body=None, raise_for_status: bool = True
    ):

        if not self.verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        response = self.session.request(
            url=url, data=body, params=params, method=method, verify=self.verify
        )
        if raise_for_status:
            response.raise_for_status()
        return response

    def _get_system_status(self) -> dict:
        self._login()
        base_url = "system/status"
        url = f"https://{self.host}/{self._monitor_base_url}/{base_url}"

        result = self.session.get(url=url, headers=self.headers, verify=self.verify)
        self._logout()

        return result.json()["results"]
