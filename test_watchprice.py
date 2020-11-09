from django.test import TestCase
from watchprice_2 import Watchprice
from django.contrib.auth.models import User
from simulator.models import Stock


class buysellTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('jeff', '123@123.com', '123')
        self.watchprice = Watchprice()
        Stock.objects.create(code='aapl', name='Apple')

    # def test_set(self):
    #     assert self.watchprice.set('aapl', 100, self.user, 'buy') != {}
     

