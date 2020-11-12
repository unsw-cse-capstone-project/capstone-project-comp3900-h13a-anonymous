from api.historical import get_historical
from datetime import datetime
from django.test import TestCase

class test_historical(TestCase):
    def setUp(self):
        self.now = datetime.now().timestamp()

    def test_upper(self):
        assert len(get_historical('AAPL', self.now)) > 0

    def test_lower(self):
        assert len(get_historical('aapl', self.now)) > 0

    def test_invalid(self):
        assert len(get_historical('abcd', self.now)) == 0
