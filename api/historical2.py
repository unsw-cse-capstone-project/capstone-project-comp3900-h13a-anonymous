########################
## pip3 install plotly

import requests
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

#will return list of price for perdiction #D
def get_historical(code, time, path):
     now =  datetime.now().timestamp()
     now = round(now)
     df = pd.read_csv(f'https://finnhub.io/api/v1/stock/candle?symbol={code}&resolution=D&from={time}&to={now}&token=btkkvsv48v6r1ugbcp70&format=csv')
     date = []
     for d in df['t']:
          date.append(datetime.fromtimestamp(d))
     fig = go.Figure(data=[go.Candlestick(x=date,
                    open=df['o'], high=df['h'],
                    low=df['l'], close=df['c'])
                         ])

     fig.update_layout(xaxis_rangeslider_visible=False)
     
     fig.write_html("sample_historical_data.html", full_html = False)
     return list(df['c'])
def get_historical_data(code,time):
     now =  datetime.now().timestamp()
     now = round(now)
     df = pd.read_csv(f'https://finnhub.io/api/v1/stock/candle?symbol={code}&resolution=D&from={time}&to={now}&token=btkkvsv48v6r1ugbcp70&format=csv')
     return list(df['c'])
if __name__ == "__main__":
     get_historical("AAPL", 1601577795, "sample_historical_data.html")