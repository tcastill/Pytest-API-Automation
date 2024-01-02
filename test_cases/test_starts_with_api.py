import logging
import pytest
import allure
import requests

from config import config_vars as config
from test_cases.allure_report import Allure as al

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ApiInternalError(Exception):
    pass


class SpecialCharacterError(Exception):
    pass


@pytest.fixture(scope="module")
@allure.title("Prepare for the test")
def set_up():
    ...  # set up
    logger.info("This will execute before test cases")
    yield
    ...  # tear down
    logger.info("Tests has completed")


@pytest.mark.sw
@allure.title("API Stars With Query")
@pytest.mark.parametrize("test_word, error", [("t??k", "The API returned a 500 error"),
                                              ("pa?r", "The API returned a 500 error"),
                                              ("pa??", "The API returned a 500 error"),
                                              ("?aI?", "The API returned a 500 error"),
                                              ("l?op", "The API returned a 500 error"),
                                              ])
def test_starts_with(set_up, test_word, error):
    response = requests.get(
        f"{config.BASE_URL}{config.SPELLED_WITH_FILTER}{test_word}")
    response_body = response.json()
    assert response.status_code == config.SUCCESSFUL

    words = []
    valid_words = []
    datamuse_count = 0
    dict_count = 0
    suggested_values = [[item_word[config.WORD],
                         item_word[config.SCORE]] for item_word in response_body]
    for word, score in suggested_values:
        first, *other, fourth = final_word = word.lower().replace(" ", "")
        words.append([word, score])
        datamuse_count += 1
        if test_word[0] != '?':
            assert first == test_word[0], "First letter did not start with the correct query"
        if test_word[-1] != '?':
            assert fourth == test_word[-1], "Last letter did not end with with the correct query"
        # assert final_word.isalnum(), "The letters must be valid characters"

        characters = config.SPECIAL_CHARACTERS
        for character in characters:
            if character in word:
                raise SpecialCharacterError(
                    f'The string has a special character: {character}')

        assert len(final_word) == len(
            test_word), "All letters did not return the same letter count"
        dictionary_response = requests.get(
            f"{config.DICTIONARY_URI}{final_word}")
        if dictionary_response.status_code == config.SUCCESSFUL:
            dict_count += 1
            valid_words.append([final_word,
                                dictionary_response.json()[0][config.MEANINGS][0][config.DEFINITIONS][0][
                                    config.DEFINITION]])
        if dictionary_response.status_code == config.INTERNAL_ERROR:
            raise ApiInternalError('The API returned a 500 error')

    al.add_text(response, response.request.url)
    al.build_chart(words, config.WORD.capitalize(),
                   config.SCORE.capitalize(), f"{datamuse_count} total Datamuse Words")
    al.build_chart(valid_words, config.NAME,
                   config.DESCRIPTION, f"{dict_count} Valid Dictionary Words")
