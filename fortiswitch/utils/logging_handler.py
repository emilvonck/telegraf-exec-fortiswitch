#!/usr/bin/python3


"""Code written by Gustav Larsson. Logging setup and handler."""

import logging
import os
import sys

try:
    LOGLEVEL = os.environ["LOGLEVEL"]

except KeyError:
    LOGLEVEL = "INFO"


class LogHandler:
    """Class to handle logging."""

    def __init__(self, instance):
        """Set upp logger."""
        logging.basicConfig(
            stream=sys.stdout,
            level=LOGLEVEL,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.logger = logging.getLogger(instance)

    def format_logs(self, level, message_type, message, **kwargs):
        """Help format messages."""
        info = {
            "type": message_type,
            "message": message,
        }

        for k, v in kwargs.items():
            info.update({k: v})

        self.logger.log(level, info)
