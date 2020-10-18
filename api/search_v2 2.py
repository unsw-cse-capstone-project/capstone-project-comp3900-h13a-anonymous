import requests

class Api(): 
    def __init__(self):
        self.token = 'btkkvsv48v6r1ugbcp70'
        self.base_url = 'https://finnhub.io/api/v1/'

    def search(self, code):
        r = requests.get(f'{self.base_url}quote?symbol={code}&token={self.token}')
        if r.json()['t'] == 0:
            return "The stock code you searched was invalid"
        profile = self.company_profile(code)
        print(profile)
        search_result = r.json()
        search_result["code"] = code
        search_result["name"] = profile["name"]
        change = (search_result['c'] - search_result['pc']) / search_result['pc']
        search_result["change"] = round(change,4)

        return search_result

    def company_profile(self, code):
        r = requests.get(f'{self.base_url}stock/profile2?symbol={code}&token={self.token}')
        if r.json()['name'] == "":
            return "invalid stock code"
        return r.json()

if __name__ == '__main__':
    api = Api()
    print(api.search('AAPL'))