########################
## pip3 install plotly
## pip3 install psutil


# import requests
# r = requests.get('https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=1&from=1572651390&to=1572910590&token=btkkvsv48v6r1ugbcp70')
# print(r.json())


import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['AAPL.Open'], high=df['AAPL.High'],
                low=df['AAPL.Low'], close=df['AAPL.Close'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()
fig.write_image("graph.jpg")