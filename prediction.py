from sklearn import linear_model
from api.historical import *
import numpy as np
import random
from datetime import date, timedelta
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def predict(code, day):
    result = []
    reg = linear_model.BayesianRidge()
    reg2 = linear_model.BayesianRidge()
    reg3 = linear_model.BayesianRidge()
    reg4 = linear_model.BayesianRidge()
    today = datetime.today()
    tgt = today - timedelta(days=day)
    ts = time.mktime(tgt.timetuple())
    data = get_historical_data(code, ts)
    data1 = data[0]
    data2 = data[1]
    data3 = data[2]
    data4 = data[3]
    
    x = []
    for i in range(0, len(data1)):
        x.append(i)
    y = [0]*len(data1)
    newX = np.vstack((x,y)).T
    reg.fit(newX,data1)

    x = []
    for i in range(0, len(data1)):
        x.append(i)
    y = [0]*len(data2)
    newX = np.vstack((x,y)).T
    reg2.fit(newX,data2)

    x = []
    for i in range(0, len(data1)):
        x.append(i)
    y = [0]*len(data3)
    newX = np.vstack((x,y)).T
    reg3.fit(newX,data3)

    x = []
    for i in range(0, len(data4)):
        x.append(i)
    y = [0]*len(data4)
    newX = np.vstack((x,y)).T
    reg4.fit(newX,data4)

    for i in range(0,day):
        da = date.today() + timedelta(days=i+1)
        #sb =  random.uniform(-3,2)
        pre = float(reg.predict([[i+1+len(data1),0]]) + reg2.predict([[i+1+len(data1),0]]) - reg3.predict([[i+1+len(data1),0]]) + reg4.predict([[i+1+len(data1),0]]))/2
        result.append((da,pre))
    print(result)
    return result


if __name__ == "__main__":
    predict("BABA", 30)
