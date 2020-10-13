# https://pypi.org/project/websocket_client/
import websocket

token = 'btkkvsv48v6r1ugbcp70'
code = None
data = None

def search(c):
    global code
    global token
    global data
    code = c
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token={}".format(token),
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()
    return data

def on_message(ws, message):
    global data
    data = message
    ws.keep_running=False


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    global code
    ws.send('{"type":"subscribe","symbol":"'+code+'"}')
    # ws.send('{"type":"subscribe","symbol":"AAPL"}')
    # ws.send('{"type":"subscribe","symbol":"AMZN"}')
    # ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')


if __name__ == "__main__":
    print(search("BINANCE:BTCUSDT"))
