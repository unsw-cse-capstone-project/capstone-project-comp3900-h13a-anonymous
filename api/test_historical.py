from api.historical2 import get_historical
from datetime import datetime
from django.test import TestCase

class test_historical(TestCase):
    def setUp(self):
        self.now = datetime.now().timestamp()

    def test_upper(self):
        assert get_historical('AAPL', self.now) is not None

    def test_lower(self):
        assert get_historical('aapl', self.now) is not None

    def test_invalidName(self):
        assert get_historical('apl', self.now) is None
