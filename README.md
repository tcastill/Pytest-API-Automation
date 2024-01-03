# API Automation using Pytest

This automation will demonstrate how to utilize the Pytest and Python testing framework to automate two endpoints: https://dictionaryapi.dev/ and https://www.datamuse.com/api/.

The dictionary api is used to cross-reference words suggested by the datamuse api to determine if they are legitimate. All of Datamuse's available endpoints will be covered by this code.

- Means like 
- Sounds Like
- Spelled Like
- Related Word

## Technology Stack

Python 3

[pytest](https://docs.pytest.org/en/stable/)

[Allure Reporting](http://allure.qatools.ru/)

## Packages required to run

The following requirements must be installed for this framework to run. Run the command below.
```bash
pip install -r requirements.txt
```

## Usage
Running the tests can be run by python scripts for tests starting with "run_"
```run
python run_tests.py
```

## Invocations
How to run in the command line
```run
pytest test_sounds_like_api.py               # run single file
pytest test_cases                            # run whole folder
-s                                           # print out all the print logs while test execution
-v                                           # verbose mode to show the test case name in the console
-x                                           # stop after first failure
-m name_of_test                              # test name labelled after '@pytest.mark'. e.g. @pytest.mark.sl will be -m sl
-k name_of_test name_of_folder               # e.g.: pytest -k test_sounds_like test_cases  will run one test case in the folder
--maxfail=2                                  # stop after two failure
--durations=10 --durations-min=1.0           # to get a list of the slowest 10 test durations over 1.0s long
```
Parallel options
```run
-n auto                                      # will distribute number of workers. e.g. browser windows or api calls
--max-worker-restart number                  # option to limit the number of workers restarts that are allowed
                                             # to disable: --max-worker-restart 0
--maxprocesses=maxprocesses: limit the maximum number of workers to process the tests.
--max-worker-restart: maximum number of workers that can be restarted when crashed (set to zero to disable this feature).
```
Rerun options
```run
--reruns 10                                  # will reruns 10x if failed 
--reruns-delay 5                             # will add a delay of 5ml after a failed run
--dist worksteal
```
## Tag tests
Skip tagging tests
```run
Skip by tag:                                 # @pytest.mark.skip("Skipping as this functionality is broken. Develper is fixing it")
Skip by condition:                           # @pytest.mark.skipif(a>100), reason = "Skipping due to limit reached")    
```