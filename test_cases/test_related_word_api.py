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
@pytest.mark.parametrize("query, related_word", [("ocean", "open"),
                                                 ("tears", "many"),
                                                 ("unhappy", "happy"),
                                                 ("starwars", "[]"),
                                                 ("JUMPING", "high"),
                                                 ("fwfwf", "[]]")
                                                 ])
def test_related_word(set_up, query, related_word):
    response = requests.get(f"{config.BASE_URL}{config.RELATED_WORD_FILTER}{query}")
    assert response.status_code == 200
    response_body = response.json()
    assert response.headers[
               config.CONTENT_TYPE] == config.APPLICATION_JSON, "Headers are not matching for application json"

    suggested_count = 0
    words = []
    for word in response_body:
        words.append([word[config.WORD], word[config.SCORE]])
        suggested_count += 1

    al.build_chart(words, config.WORD.capitalize(),
                   config.SCORE.capitalize(), f"{suggested_count} total suggested sounds like words")
