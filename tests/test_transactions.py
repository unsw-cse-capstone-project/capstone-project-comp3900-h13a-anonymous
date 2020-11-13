from django.test import TestCase
from modules.transactions import *
import modules.buy_sell as buy_sell

class TransactionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('jeff', '123@123.com', '123')
        buy_sell.buy('aapl', 2, self.user)
        buy_sell.buy('aapl', 2, self.user)
        buy_sell.buy('aapl', 2, self.user)
        buy_sell.sell('aapl', 3, self.user)
        buy_sell.buy('amzn', 2, self.user)
        buy_sell.sell('amzn', 2, self.user)

    def test_get_user_transactions(self):
        transactions_list = get_user_transactions(self.user)
        assert len(transactions_list) == 6

        assert transactions_list[0]['code'] == 'AMZN'
        assert transactions_list[0]['units'] == 2
        assert transactions_list[0]['action'] == "sell"

        assert transactions_list[1]['code'] == 'AMZN'
        assert transactions_list[1]['units'] == 2
        assert transactions_list[1]['action'] == "buy"

        assert transactions_list[2]['code'] == 'AAPL'
        assert transactions_list[2]['units'] == 3
        assert transactions_list[2]['action'] == "sell"

        assert transactions_list[3]['code'] == 'AAPL'
        assert transactions_list[3]['units'] == 2
        assert transactions_list[3]['action'] == "buy"
        
        assert transactions_list[4]['code'] == 'AAPL'
        assert transactions_list[4]['units'] == 2
        assert transactions_list[4]['action'] == "buy"

        assert transactions_list[5]['code'] == 'AAPL'
        assert transactions_list[5]['units'] == 2
        assert transactions_list[5]['action'] == "buy"

