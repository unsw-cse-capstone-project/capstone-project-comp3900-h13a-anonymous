########################
# pip3 install plotly

import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_historical(code, time):

    try:
        print(time)
        time = datetime.fromtimestamp(int(float(time)))
        time = time - timedelta(weeks=1)
        time = datetime.timestamp(time)
        time=round(time)
        now = datetime.now().timestamp()
        df = pd.read_csv(
            f'https://finnhub.io/api/v1/stock/candle?symbol={code}&resolution=1&from={time}&to={now}&token=btkkvsv48v6r1ugbcp70&format=csv')

        print(df)

        date = []
        for d in df['t']:
            date.append(datetime.fromtimestamp(d))
        fig = go.Figure(data=[go.Candlestick(x=date,
                                            open=df['o'], high=df['h'],
                                            low=df['l'], close=df['c'])
                            ])

        fig.write_html("simulator/templates/simulator/graph.html")
    except:
        pass



if __name__ == "__main__":
    get_historical("AAPL", 1604015790)
