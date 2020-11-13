from django.test import TestCase
from modules.watchlist import *

class watchlistTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('jeff', '123@123.com', '123')

    def test_add(self):
        assert add('aapl', self.user)['success'] == "Stock AAPL added to your watchlist"

    def test_add_duplicate(self):
        add('aapl', self.user)
        assert add('aapl', self.user)['error'] == "Stock AAPL is already in your watchlist"

    def test_list(self):
        lis, msg = list_watchlist(self.user, {})
        assert lis == []

    def test_list(self):
        add('aapl', self.user)
        lis, msg = list_watchlist(self.user, {})
        assert lis != []

    def test_remove(self):
        add('aapl', self.user)
        remove('aapl', self.user)
        lis, msg = list_watchlist(self.user, {})
        assert lis == []

