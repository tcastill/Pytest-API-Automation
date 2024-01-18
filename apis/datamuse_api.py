import logging
import requests

from config import config_vars as config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Datamuse:
    def spelled_with(word):
        response = requests.get(
            f"{config.BASE_URL}{config.SPELLED_WITH_FILTER}{word}")
        assert response.ok is True
        return response
