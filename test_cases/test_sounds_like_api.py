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
    print("This wille execute before test cases")
    yield
    ...  # tear down
    print("Tests has completed")


@pytest.mark.sl
def test_sounds_like(set_up):
    query = 'jirraf'
    response = requests.get(f"{config.BASE_URL}{config.SOUND_LIKE_FILTER}{query}")
    assert response.status_code == 200
    response_body = response.json()
    assert response.headers[
               config.CONTENT_TYPE] == config.APPLICATION_JSON, "Headers are not matching for application json"
    assert response_body[0][config.WORD] == "giraffe", "Word did not match for the first entry"
    assert response_body[0][config.NUMBER_OF_SYLLABULS] >= 2, "Numbers did not match"

    words = []
    for word in response_body:
        words.append([word[config.WORD], word[config.SCORE]])

    # define header names
    col_names = [config.WORD.capitalize(), config.SCORE.capitalize()]

    # display table
    # print(tabulate(words, headers=col_names))
    # allure.attach(tabulate(words, headers=col_names), name="CSV example", attachment_type=attachment_type.TEXT)
    allure.attach(
        tabulate(words, headers=col_names),
        'Chart',
        attachment_type=allure.attachment_type.TEXT,
        extension='txt')
    allure.attach(
        body=response.text.encode('utf8'),
        name=f'the thing'
             f'{response.request.url}',
        attachment_type=allure.attachment_type.TEXT,
        extension='txt')
