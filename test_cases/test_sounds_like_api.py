import logging
import pytest
import allure
import requests

from config import config_vars as config
from test_cases.allure_report import Allure as al

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture(scope="module")
@allure.title("Prepare for the test")
def set_up():
    ...  # set up
    print("This wille execute before test cases")
    yield
    ...  # tear down
    print("Tests has completed")


@pytest.mark.sl
@allure.title("API Sounds Like Query")
@pytest.mark.parametrize("query, sound_like", [("jirraf", "giraffe"),
                                               ("Chocolate", "chocolate"),
                                               ("kichken", "kickin"),
                                                    ("MRBL", "marble"),
                                                    ("iron mein", "ironman"),
                                                    ("numatic", "pneumatic")
                                                    ])
def test_sounds_like(set_up, query, sound_like):
    response = requests.get(f"{config.BASE_URL}{config.SOUND_LIKE_FILTER}{query}")
    assert response.status_code == 200
    response_body = response.json()
    assert response.headers[
               config.CONTENT_TYPE] == config.APPLICATION_JSON, "Headers are not matching for application json"
    assert response_body[0][config.WORD].lower() == sound_like, "Word did not match for the first entry"
    assert response_body[0][config.NUMBER_OF_SYLLABULS] >= 2, "Numbers did not match"

    suggested_count = 0
    words = []
    for word in response_body:
        words.append([word[config.WORD], word[config.SCORE]])
        suggested_count += 1

    al.build_chart(words, config.WORD.capitalize(),
                   config.SCORE.capitalize(), f"{suggested_count} total suggested sounds like words")
