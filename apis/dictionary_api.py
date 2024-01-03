import logging
import requests

from config import config_vars as config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Dictionary:
    def get(word):
        response = requests.get(f"{config.DICTIONARY_URI}{word}")
        logger.info(response)
        return response
