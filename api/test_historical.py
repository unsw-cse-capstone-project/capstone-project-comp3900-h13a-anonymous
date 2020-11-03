from api.historical2 import get_historical
from datetime import datetime

now = datetime.now().timestamp()

def test_upper():
    assert get_historical('AAPL', now) is not None

def test_lower():
    assert get_historical('aapl', now) is not None

def test_invalidName():
    assert get_historical('apl', now) is None
