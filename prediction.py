from sklearn import linear_model
from api.historical2 import *
import numpy as np
import random
from datetime import date, timedelta
def prediction(code, day):
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
        sb =  random.uniform(-3,2)
        pre = float(reg.predict([[i+1+len(data),0]])) + sb
        result.append((da,pre))
    # print(result)
    return result
if __name__ == "__main__":
    prediction("AAPL", 30)