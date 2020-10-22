from django.db import models
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Create your models here.


class Stock(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def publish(self):
        self.save()

    def __str__(self):
        return self.code


class User(models.Model):
    email = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    phoneNo = models.IntegerField()
    balance = models.DecimalField(decimal_places=2, max_digits=10)



class WatchList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.CharField(max_length=30)

    def __str__(self):
        return self.date

    def plot_watchlist(self):
        now =  datetime.now().timestamp()
        df = pd.read_csv(f'https://finnhub.io/api/v1/stock/candle?symbol={self.code.code}&resolution=1&from={self.date}&to={now}&token=btkkvsv48v6r1ugbcp70&format=csv')

        print(df)

        date = []
        for d in df['t']:
            date.append(datetime.fromtimestamp(d))
        fig = go.Figure(data=[go.Candlestick(x=date,
                    open=df['o'], high=df['h'],
                    low=df['l'], close=df['c'])
                            ])

        fig.update_layout(xaxis_rangeslider_visible=False)

        return fig.write_html("sample_historical_data.html", full_html = False)


class Purchase(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    dateBuy = models.DateTimeField()
    dateSell = models.DateTimeField()
    unitBuy = models.PositiveIntegerField()
    unitSell = models.PositiveIntegerField()
