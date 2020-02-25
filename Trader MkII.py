#Updated Main Strategy

import datetime
import random
from datetime import date
import CAC40 as cac
import Indicators as ind
import Visuals as vs
import Filters as fil
import Retrieval as get

cac40 = cac.stocks40()
sbf120 = cac.stocks120()
date1 = date.today()-datetime.timedelta(10)
date2 = date.today()+datetime.timedelta(1)

def risklistintra():
    #returns a list of stock risks.
    risks=[]
    for x in sbf120:
        a = get.intraday(x, date1, date2)
        risks.append(ind.risk_SD_int(a))
    return risks

def quicktestintra(coeff):
    #For a random stock, shows the smoothed curve, as well as returning 
    #various sureness and risk indicators
    stock = sbf120[random.randint(0,len(sbf120))]
    a = get.intraday(stock , date1, date2)
    print(stock)
    b = fil.KF(a,coeff)
    vs.plotstock(a,b,cac.name(stock))
    print('Smoothing Sureness: ' + str(ind.kalsure(a)))
    print('Trend sureness: ' + str(ind.trendsure(a)))
    print('Risk: ' + str(ind.risk_SD(a)))
    
def predictKAL (serie, coeff):
    #Prediction using a kalman filter and a simple second order expansion
    smooth = fil.KF(serie,coeff)
    x1,x2,x3 = smooth[-1],smooth[-2],smooth[-3]
    dx = x1-x2 + 0.5*((x1-x2)-(x2-x3)) 
    return 255*(((x1+dx)/x1)-1)

def nextintradayKF (serie,margin):
    #Establishes indicators and predictions for a stock, then based on the
    #indicators and the strength of the prediction, returns an order.
    predict = predictKAL(serie,0.005)
    if predict > 0.01*margin:
        trendsure = ind.trendsure(serie)
        kalsure = ind.kalsure(serie)
        risk = ind.risk_SD(serie)
        if abs(kalsure) > 0.1 and risk < 0.3:
            return (True , 'BUY', kalsure , trendsure)
        else:
            return (False,False,False)
    elif predict < -0.01*margin:   
        trendsure = ind.trendsure(serie)
        kalsure = ind.kalsure(serie)
        risk = ind.risk_SD(serie)
        if abs(kalsure) > 0.1 and risk < 0.3:
            return (True , 'SELL', kalsure , trendsure)
        else:
            return (False,False,False)
    else:
        return (False,False,False)
    
def day_predict_MkIII(margin, day=date2):
    #For each stock, returns the next-day predictions for the kalman filter
    for i in sbf120:
        a = nextintradayKF(get.intraday(i,date1,day), margin)
        if a[0]:
            print(a[1] + ' ' + cac.name(i) + ' ' + i + ' ' + str(a[2]) + ' ' +
                  str(a[3]))
        else:
            pass
        
def show(stock, coeff=0.005):
    a = get.intraday(stock , date1, date2)
    b = fil.KF(a,coeff)
    vs.plotstock(a,b,cac.name(stock))
    print('Smoothing Sureness: ' + str(ind.kalsure(a)))
    print('Trend sureness: ' + str(ind.trendsure(a)))
    print('Risk: ' + str(ind.risk_SD(a)))