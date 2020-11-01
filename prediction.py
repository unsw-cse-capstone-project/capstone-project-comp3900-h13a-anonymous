from sklearn import linear_model
from api.historical2 import *
import numpy as np
from datetime import date, timedelta
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def predict(code, day):
    result = []
    reg = linear_model.BayesianRidge()
    data = get_historical_data(code,1572447323)
    x = []
    for i in range(0, len(data)):
        x.append(i)
    y = [0]*len(data)
    newX = np.vstack((x,y)).T
    reg.fit(newX,data)
    for i in range(0,day):
        da = date.today() + timedelta(days=i+1)
        pre = float(reg.predict([[i+1+len(data),0]]))
        result.append((da,pre))
    #print(result)
    
    day = []
    price = []
    for i in result:
        day.append(i[0]);
        price.append(i[1]);
    
    print(day)
    print(price)

    return result
if __name__ == "__main__":
    predict("AAPL", 30)