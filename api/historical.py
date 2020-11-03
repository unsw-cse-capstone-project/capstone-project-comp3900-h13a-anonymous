########################
## pip3 install plotly

import os
import requests
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_historical():
     time = 1601577795
     code = "AAPL"
     now =  datetime.now().timestamp()
     df = pd.read_csv(f'https://finnhub.io/api/v1/stock/candle?symbol={code}&resolution=1&from={time}&to={now}&token=btkkvsv48v6r1ugbcp70&format=csv')

     high = df['h'].tolist()
     low = df['l'].tolist()
     closePrice = df['c'].tolist()
     openPrice = df['o'].tolist()

     date = []
     for d in df['t'].tolist():
          date.append(datetime.fromtimestamp(d))

     print(high)
          

if __name__ == "__main__":
     get_historical()