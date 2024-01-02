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
def test_starts_with(set_up):
    query = 't??k'
    response = requests.get(f"{config.BASE_URL}{config.SPELLED_WITH_FILTER}{query}")
    response_body = response.json()

    words = []
    valid_words = []
    assert response.status_code == config.SUCCESSFUL

    # suggested_values = list(map(lambda item_word: [item_word[config.WORD], item_word[config.SCORE]], response_body))
    suggested_values = [[item_word[config.WORD], item_word[config.SCORE]] for item_word in response_body]
    for word, score in suggested_values:
        first, *other, fourth = word.lower()
        words.append([word, score])
        assert first == 't', "First letter did not start with a t"
        assert fourth == 'k', "First letter did not start with a k"
        assert word.isalpha(), "The letters must be characters"
        assert len(word) == 4, "All letters should equal 4"

        dictionary_response = requests.get(f"{config.DICTIONARY_URI}{word}")
        if dictionary_response.status_code == config.SUCCESSFUL:
            valid_words.append([word, dictionary_response.json()[0]['meanings'][0]['definitions'][0]['definition']])
        if dictionary_response.status_code == config.INTERNAL_ERROR:
            raise api_internal_error("The API returned a 500 error")
    al.add_text(response, response.request.url)

    al.build_chart(words, config.WORD.capitalize(), config.SCORE.capitalize(), "Datamuse Words")
    al.build_chart(valid_words, "name", "description", "Valid Dictionary Words")
