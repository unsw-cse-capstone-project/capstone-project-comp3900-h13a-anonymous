import requests

token = 'btkkvsv48v6r1ugbcp70'

def search(code):
    r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={code}&token={token}')
    if r.json()['t'] == 0:
        return "invalid stock code"
    return r.json()

if __name__ == '__main__':
    print(search('AAPL'))