############################
## HOW TO RUN
## type the command below
## py.test
## for coverage report run
## py.test --cov=. --cov-report html

from api.search_v2 import Api

api = Api()

def test_upper():
    assert api.search("AAPL") != {}

def test_lower():
    assert api.search("aapl") != {}

def test_invalid():
    assert api.search("abcd") == "The stock code you searched was invalid"
    assert api.search("goog") == "The stock code you searched was invalid"
    