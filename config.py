import logging
from logging.handlers import RotatingFileHandler

import yaml


class Config:

    def __init__(self, path="./config.yml"):
        # TODO: Load config, create logger.
        self._config = yaml.safe_load(open(path))

        self.logger = logging.getLogger(__name__)
        level = logging.WARNING if not self.debug else logging.DEBUG
        self.logger.setLevel(level)

        format_ = "%(asctime)s - [%(levelname)s] - %(message)s"
        formatter = logging.Formatter(format_)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = RotatingFileHandler("bot.log", maxBytes=50000000)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.debug("Config and Logger loaded!")

    @property
    def debug(self):
        return self._config["debug"]

    @property
    def remove(self):
        return self._config["remove"]

    @property
    def removal_reason(self):
        return self._config["removal_reason"]

    @property
    def human_review(self):
        return self._config["human_review"]

    @property
    def human_review_report(self):
        return self._config["human_review_report"]
