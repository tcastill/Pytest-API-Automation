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


@pytest.mark.sw
@allure.title("API Stars With Query")
def test_starts_with(set_up):
    query = 't??k'
    response = requests.get(f"{config.BASE_URL}{config.SPELLED_WITH_FILTER}{query}")
    response_body = response.json()

    if response.status_code == 200:
        print("Checking words that starts with")
        assert query[0].lower() == 't', "First letter did not start with a t"
        assert query[-1].lower() == 'k', "First letter did not start with a k"

    allure_add_text(response)

    words = []
    for word in response_body:
        words.append([word[config.WORD], word[config.SCORE]])
    build_chart(words)


def build_chart(data):
    col_names = [config.WORD.capitalize(), config.SCORE.capitalize()]
    allure.attach(
        tabulate(data, headers=col_names),
        'Chart',
        attachment_type=allure.attachment_type.TEXT,
        extension='txt')


def allure_add_text(data):
    allure.attach(
        body=data.text.encode('utf8'),
        name=f'the thing'
             f'{data.request.url}',
        attachment_type=allure.attachment_type.TEXT,
        extension='txt')
