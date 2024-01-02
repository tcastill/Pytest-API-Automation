import allure

from config import config_vars as config
from tabulate import tabulate


class Allure:

    @staticmethod
    def add_text(data, request_url):
        allure.attach(
            body=data.text.encode(config.UTF8),
            name=f'Request URL'
                 f'{request_url}',
            attachment_type=allure.attachment_type.TEXT,
            extension=config.TXT_TYPE)

    @staticmethod
    def build_chart(data, header1, header2, chart_name):
        col_names = [header1, header2]
        allure.attach(
            tabulate(data, headers=col_names),
            chart_name,
            attachment_type=allure.attachment_type.TEXT,
            extension=config.TXT_TYPE)
