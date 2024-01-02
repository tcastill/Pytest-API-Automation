#!/usr/bin/env python3
import os
import shutil

from os import path

if str(path.exists('allure_test_result')):
    shutil.rmtree('allure_test_result', ignore_errors=True)

#Run test
#os.system('py.test -v -n 5 -m sl --durations=3 --cov=. --alluredir=allure_test_result --reruns 10 --reruns-delay 5')

#Run test this will show all the print statements with -s
os.system('py.test -s -v --durations=3 --cov --cov-report html --html-report=./report --alluredir=allure_test_result')

#Run allure report
os.system('allure serve allure_test_result')