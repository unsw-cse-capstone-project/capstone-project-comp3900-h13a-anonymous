from search_v2 import Api
import threading
import time
watch = {"AAPL" : 200, "AMZN":100}


def check(code, price):
    count = 0
    while True:
        api = Api()
        tgt = api.search(code)
        count += 1
        print(count)
        try: 

            print(tgt['c'])
            a = tgt['c']
            if a >= price :
                return
        except:
            print("Exception")


if __name__ == "__main__":
    for sb in watch.keys():
        #print ("hello")
        th = threading.Thread(target=check, args=(sb, watch[sb]))
        #th.setDaemon(True)
        th.start()


# print("fewiofjwe")


# exit()
# print("fewiofjwe")
