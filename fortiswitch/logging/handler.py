#!/usr/bin/python3

"""Code written by Gustav Larsson. Logging setup and handler."""

import logging
import os
import sys
from typing import Any

try:
    LOGLEVEL = os.environ["LOGLEVEL"]

except KeyError:
    LOGLEVEL = "INFO"


class LogHandler:
    """Class to handle logging."""

    def __init__(self, instance):
        """Set up logger."""
        logging.basicConfig(
            stream=sys.stdout,
            level=LOGLEVEL,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.logger = logging.getLogger(instance)

    def format_logs(self, level: int, message_type: Any, message: Any, **kwargs):
        """Log formatting.

        Args:
            level (int): Log level.
            message_type (str: Message type string.
            message (str): Message string.
        """
        info = {"type": message_type, "message": message}
        for key, value in kwargs.items():
            info.update({key: value})

        self.logger.log(level, info)
