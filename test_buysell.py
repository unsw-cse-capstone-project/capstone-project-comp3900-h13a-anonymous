from django.test import TestCase
from buy_sell import *
from django.contrib.auth.models import User


class buysellTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('jeff', '123@123.com', '123')

    def test_init(self):
        assert self.user.profile.balance == 10000

    def test_buy(self):
        balance = self.user.profile.balance
        buy('aapl', 1, self.user)
        assert self.user.profile.balance < balance
    
    def test_sell(self):
        buy('aapl', 1, self.user)
        balance = self.user.profile.balance
        sell('aapl', 1, self.user)
        assert self.user.profile.balance > balance

    def test_insufficientbalance(self):
        buy('aapl', 10000, self.user)
        assert self.user.profile.balance == 10000

    def test_insufficientshare(self):
        buy('aapl', 1, self.user)
        balance = self.user.profile.balance
        sell('aapl', 2, self.user)
        assert self.user.profile.balance == balance


