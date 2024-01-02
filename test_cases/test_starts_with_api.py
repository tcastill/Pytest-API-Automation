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
    logger.info("This will execute before test cases")
    yield
    ...  # tear down
    logger.info("Tests has completed")


def api_internal_error(exception):
    pass


@pytest.mark.sw
@allure.title("API Stars With Query")
@pytest.mark.parametrize("test_word, error", [("t??k", "The API returned a 500 error")])
def test_starts_with(set_up, test_word, error):
    response = requests.get(f"{config.BASE_URL}{config.SPELLED_WITH_FILTER}{test_word}")
    response_body = response.json()

    words = []
    valid_words = []
    assert response.status_code == config.SUCCESSFUL

    suggested_values = [[item_word[config.WORD], item_word[config.SCORE]] for item_word in response_body]
    for word, score in suggested_values:
        first, *other, fourth = word.lower()
        words.append([word, score])
        assert first == test_word[0], "First letter did not start with a t"
        assert fourth == test_word[-1], "First letter did not start with a k"
        assert word.isalpha(), "The letters must be valid characters"
        assert len(word) == len(test_word), "All letters did not return the same letter count"

        dictionary_response = requests.get(f"{config.DICTIONARY_URI}{word}")
        if dictionary_response.status_code == config.SUCCESSFUL:
            valid_words.append([word,
                                dictionary_response.json()[0][config.MEANINGS][0][config.DEFINITIONS][0][config.DEFINITION]])
        if dictionary_response.status_code == config.INTERNAL_ERROR:
            raise api_internal_error(error)

    al.add_text(response, response.request.url)
    al.build_chart(words, config.WORD.capitalize(), config.SCORE.capitalize(), "Datamuse Words")
    al.build_chart(valid_words, config.NAME, config.DESCRIPTION, "Valid Dictionary Words")
