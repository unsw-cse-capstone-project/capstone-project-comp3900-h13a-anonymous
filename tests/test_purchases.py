from django.test import TestCase
from modules.purchases import *
import modules.buy_sell as buy_sell
from django.contrib.auth.models import User


class purchasesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('jeff', '123@123.com', '123')
        buy_sell.buy('aapl', 2, self.user)
        buy_sell.buy('aapl', 2, self.user)
        buy_sell.buy('aapl', 2, self.user)
        buy_sell.sell('aapl', 3, self.user)
        buy_sell.buy('amzn', 2, self.user)
        buy_sell.sell('amzn', 2, self.user)
        

    def test_get_total_owned_units(self):
        total_owned_units = get_total_owned_units(self.user, 'AAPL')
        assert total_owned_units == 3

    def test_get_unsold_purhases(self):
        unsold_purhases = get_unsold_purhases(self.user, 'AAPL')
        assert len(unsold_purhases) == 2

    def test_get_unique_purchases_codes(self):
        upc_include_sold = get_unique_purchases_codes(self.user, True)
        upc = get_unique_purchases_codes(self.user, False)

        assert len(upc_include_sold) == 2
        assert "AAPL" in upc_include_sold
        assert "AMZN" in upc_include_sold

        assert len(upc) == 1
        assert "AAPL" in upc
        assert "AMZN" not in upc

    def test_get_purchases_info(self):
        ps_include_sold, messages = get_purchases_info(self.user, True)
        ps, messages = get_purchases_info(self.user, False)

        assert len(ps_include_sold) == 4
        assert len(ps) == 2

    def test_get_portfolio_info(self):
        port, total_portfolio_profit, messages = get_portfolio_info(self.user)

        assert len(port) == 1
        assert port[0]['code'] == 'AAPL'
        assert port[0]['noPurchases'] == 2
        assert port[0]['totalUnits'] == 3
        assert total_portfolio_profit is not None
