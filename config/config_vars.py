# Automation
NUM_RUNS = 1
TEST_SKIP = True

# API
APPLICATION_JSON = 'application/json'
CONTENT_TYPE = 'Content-Type'
TXT_TYPE = 'txt'
MEANINGS = 'meanings'
DEFINITION = 'definition'
DEFINITIONS = 'definitions'

# ENDPOINTS
DICTIONARY_URI = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
BASE_URL = 'https://api.datamuse.com/words'
MEANING_FILTER = '?ml='
RELATED_WORD_FILTER = '?rel_jjb='
SOUND_LIKE_FILTER = '?sl='
SPELLED_WITH_FILTER = '?sp='
ADJ_DESCRIBED_FILTER = '?rel_jjb='
FOLLOW_WITH = '?lc='
SUGGESTIVE_FILTER = '/sug?s='

# STATUS CODES
SUCCESSFUL = 200
REDIRECTION_ERROR = 300
NOT_FOUND_ERROR = 404
INTERNAL_ERROR = 500
UTF8 = 'utf8'

# REST CHARACTERISTICS
WORD = 'word'
SCORE = 'score'
NUMBER_OF_SYLLABULS = 'numSyllables'
NAME = 'name'
DESCRIPTION = 'description'
QUESTION_MARK = '?'

# Restricted Characters
SPECIAL_CHARACTERS = '!@#$%^&*()+?_=,<>/'
