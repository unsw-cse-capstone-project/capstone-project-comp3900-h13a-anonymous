from django.test import TestCase
from modules.leaderboard import *
import modules.buy_sell as buy_sell
from django.contrib.auth.models import User


class leaderboardTest(TestCase):

    def setUp(self):
        self.userJeff = User.objects.create_user('jeff', '123@123.com', '123')
        buy_sell.buy('aapl', 2, self.userJeff)
        self.userRiley = User.objects.create_user('riley', '456@456.com', '456')
        self.userRiley.profile.balance=9000
        self.userRiley.save()
        self.userRyan = User.objects.create_user('ryan', '789@789.com', '789')
        self.userRyan.profile.balance=11000
        self.userRyan.save()
        

    def test_get_leaderboard_info(self):
        sorted_leaderboard, messages = get_leaderboard_info()
        assert len(sorted_leaderboard) == 3
        assert sorted_leaderboard[0]['name'] == 'ryan'
        assert sorted_leaderboard[1]['name'] == 'jeff'
        assert sorted_leaderboard[2]['name'] == 'riley'

    def test_get_user_profit(self):
        cprice_cache = {}
        jeff_port_worth, cprice_cache = get_user_profit(self.userJeff, cprice_cache)
        riley_port_worth, cprice_cache = get_user_profit(self.userRiley, cprice_cache)
        ryan_port_worth, cprice_cache = get_user_profit(self.userRyan, cprice_cache)
        assert jeff_port_worth > 0
        assert riley_port_worth == 0
        assert ryan_port_worth == 0

