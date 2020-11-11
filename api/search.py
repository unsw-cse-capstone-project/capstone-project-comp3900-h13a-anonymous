import requests

'''
Exception class for finnhub API errors
'''
class FinnhubSearchError(Exception):
    def __init__(self, message):
        super().__init__(message)


'''
Class used for making api calls to finnhub
'''
class Api():
    def __init__(self):
        self.token = 'btkkvsv48v6r1ugbcp70'
        self.base_url = 'https://finnhub.io/api/v1/'

    '''
    Calls finnhub api to retrieve current price information about a stock corrospoinding to a
    given code, provided the code is valid. If an error occurs, a FinnhubSearchError
    Exception is raised

    parameters
        code : string
    returns
        search_result : {string : any}
    '''
    def search(self, code):
        try:
            r = requests.get(f"{self.base_url}quote?symbol={code}&token={self.token}")
            if r.json()['t'] == 0:
                raise FinnhubSearchError("The stock code you searched was invalid")
            profile = self.company_profile(code)
            if profile == "invalid stock code":
                raise FinnhubSearchError("The stock code you searched was invalid")
            search_result = r.json()
            search_result["code"] = code
            search_result["name"] = profile["name"]
            change = (search_result['c'] - search_result['pc']) / search_result['pc']
            search_result["change"] = round(change, 4)
            return search_result
        except Exception as e:
            print(repr(e))
            if (str(e) == "The stock code you searched was invalid") :
                raise FinnhubSearchError(str(e))
            raise FinnhubSearchError("Error with external API. Please try again")


    '''
    Calls finnhub api to retrieve current profile information about a stock corrospoinding to a
    given code, provided the code is valid

    parameters
        code : string
    returns
        search_result : {string : any}
    '''
    def company_profile(self, code):
        r = requests.get(f'{self.base_url}stock/profile2?symbol={code}&token={self.token}')
        if r.json() == {}:
            return "invalid stock code"
        return r.json()


if __name__ == '__main__':
    api = Api()
    print(api.search('aapl'))
