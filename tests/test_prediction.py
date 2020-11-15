from django.test import TestCase
from modules.prediction import *
from django.contrib.auth.models import User


class predictionTest(TestCase):

    def test_predict_upper(self):
        result1 = predict("AAPL", 30)
        assert len(result1) > 0

    def test_predict_lower(self):
        result1 = predict("aapl", 30)
        assert len(result1) > 0

    def test_invalid(self):
        try:
            result1 = predict("abcd", 30)
        except Exception as e:
            assert True
        else:
            assert False
    

    