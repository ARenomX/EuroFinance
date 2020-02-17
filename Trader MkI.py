# Main Strategies

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
date1 = datetime.date(2019,1,1)
date2 = datetime.date(2020,2,11)

def pricechecker():
    #returns most recent close price for all CAC40 stocks.
    for x in cac40:
        print(get.stock(x,date2, date2 ))
        
    
def quicktest(coeff):
    #For a random stock, shows the smoothed curve, as well as returning 
    #various sureness and risk indicators
    stock = sbf120[random.randint(0,len(sbf120))]
    a = get.stock(stock , datetime.date(2019,11,1),datetime.date(2020,1,17))
    print(stock)
    b = fil.KF(a,coeff)
    vs.plotstock(a,b,cac.name(stock))
    print('Smoothing Sureness: ' + str(ind.kalsure(a)))
    print('Trend sureness: ' + str(ind.trendsure(a)))
    print('Risk: ' + str(ind.risk_SD(a)))
    
def nextday1(stock, day = date.today()):
    #test function for evaluating accuracy of next-day prediction by comparing
    #predicted and real values.
    values = get.stock(stock, day + datetime.timedelta(days = -30), day)
    smooth = fil.WMA(values,20)
    x1,x2,x3 = smooth[-1],smooth[-2],smooth[-3]
    dx = x1-x2 + 0.5*((x1-x2)-(x2-x3))
    print(dx)
    real = get.stock(stock, day + datetime.timedelta(days = -1),
              day + datetime.timedelta(days = 1))
    realdx = real[-1]-real[-2]
    print(realdx)
    
def predictWMA (serie):
    #Prediction using a weighted moving average and a simple second order
    #expansion
    smooth = fil.WMA(serie,20)
    x1,x2,x3 = smooth[-1],smooth[-2],smooth[-3]
    dx = x1-x2 + 0.5*((x1-x2)-(x2-x3))
    return serie[-1] + dx

def predictKAL (serie, coeff):
    #Prediction using a kalman filter and a simple second order expansion
    smooth = fil.KF(serie,coeff)
    x1,x2,x3 = smooth[-1],smooth[-2],smooth[-3]
    dx = x1-x2 + 0.5*((x1-x2)-(x2-x3))
    return serie[-1] + dx

def nextday (serie):
    #Establishes indicators and predictions for a stock, then based on the
    #indicators and the strength of the prediction, returns an order.
    risk = ind.risk(serie,20)
    sure = ind.sure(serie)
    predict = predictWMA(serie)
    if risk < 30:
        if predict > serie[-1]:
            return (True , 'buy',sure)
        else:
            return (True , 'sell',sure)
    else:
        return (False,False,False)
    
def nextdayKF (serie,margin):
    #Establishes indicators and predictions for a stock, then based on the
    #indicators and the strength of the prediction, returns an order.
    predict = predictKAL(serie,0.05)
    if predict > serie[-1]*(1+margin*0.01):
        trendsure = ind.trendsure(serie)
        kalsure = ind.kalsure(serie)
        risk = ind.risk_SD(serie)
        if abs(kalsure) > 0.1 and risk < 10:
            return (True , 'BUY', kalsure , trendsure)
        else:
            return (False,False,False)
    elif predict < serie[-1]*(1-margin*0.01):   
        trendsure = ind.trendsure(serie)
        kalsure = ind.kalsure(serie)
        risk = ind.risk_SD(serie)
        if abs(kalsure) > 0.1 and risk < 10:
            return (True , 'SELL', kalsure , trendsure)
        else:
            return (False,False,False)
    else:
        return (False,False,False)
        
def day_predict(day = date.today()):
    #For each stock, returns the next-day predictions for a WMA
    for i in sbf120:
        a = nextday(get.stock(i,datetime.date(2019,12,1),day))
        if a[0]:
            print(a[1] + ' ' + cac.name(i) + ' ' + str(a[2][0]) + ' ' +
                  str(a[2][1]))
        else:
            pass
        
def day_predict_MkII(margin, day = date.today()):
    #For each stock, returns the next-day predictions for the kalman filter
    for i in sbf120:
        a = nextdayKF(get.stock(i,datetime.date(2019,11,1),day), margin)
        if a[0]:
            print(a[1] + ' ' + cac.name(i) + ' ' + str(a[2]) + ' ' +
                  str(a[3]))
        else:
            pass
        
def printstock(stock):
    #plots a given stock
    a = get.stock(stock , datetime.date(2019,1,1),datetime.date(2020,1,17))
    vs.plot(a)
    
def risklist():
    #returns a list of stock risks.
    risks=[]
    for x in sbf120:
        a = get.stock(x , datetime.date(2019,11,1),date2)
        risks.append(ind.risk_SD(a))
    return risks
        
    