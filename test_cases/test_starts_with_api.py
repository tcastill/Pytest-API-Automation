import logging
import pytest
import allure
import requests

from tabulate import tabulate
from config import config_vars as config

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
            valid_words.append(word)

    build_chart(words)
    print(valid_words)
    allure.attach(
        ' '.join(map(str, valid_words)),
        'Valid Words',
        attachment_type=allure.attachment_type.TEXT,
        extension=config.TXT_TYPE)


def build_chart(data):
    col_names = [config.WORD.capitalize(), config.SCORE.capitalize()]
    allure.attach(
        tabulate(data, headers=col_names),
        'Chart',
        attachment_type=allure.attachment_type.TEXT,
        extension=config.TXT_TYPE)


def allure_add_text(data):
    allure.attach(
        body=data.text.encode(config.UTF8),
        name=f'Request URL'
             f'{data.request.url}',
        attachment_type=allure.attachment_type.TEXT,
        extension=config.TXT_TYPE)
