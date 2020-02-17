# Indicators

import numpy as np
import Filters as fil

def sure (serie):
    #Based on the last 3 terms of the series, gives a confidence metric
    x1,x2,x3 = [serie[-(1+i)] - serie[-(2+i)] for i in range(3)]
    if np.sign(x1) == np.sign(x2) == np.sign(x3):
        return (3*np.sign(x1) , 4 * x1 + 2 * x2 + 1 * x3)
    elif np.sign(x1) == np.sign(x2) != np.sign(x3):
        return (2*np.sign(x1) , np.abs(x1 + x2) - np.abs(x3))
    else:
        return (np.sign(x1) ,  np.abs(x1) - np.abs(x2 + x3))
    
def risk (serie, n):
    #Calcuates a risk based on the squared second derivative of the series
    var = [100*serie[-(1+i)]/serie[-(2+i)] for i in range(n)]
    varvar = [(var[-(1+i)] - var[-(2+i)])**2 for i in range(n-1)]
    return sum(varvar)

def risk_SD (serie):
    #Calculates a ris based on the standard deviation of the series with
    #respect to it's smoothed mean.
    smooth = fil.KF(serie, 0.05)
    squares = [(serie[i]-smooth[i])**2 for i in range(len(smooth))]
    return sum(squares)/len(squares)

def kalsure (serie):
    #Calculates a sureness by increasing the closeness of the smoothing filter
    #until the direction of the last increment changes, returning the minimum
    #smoothing for which the direction is constant.
    smooth0 = fil.KF(serie,0)
    init_sign = np.sign(smooth0[-1]-smooth0[-2])
    cur_sign = init_sign
    smoothing_coeff = 0
    while cur_sign == init_sign and smoothing_coeff<1:
        smoothing_coeff += 0.01
        smoothn = fil.KF(serie,smoothing_coeff)
        cur_sign = np.sign(smoothn[-1]-smoothn[-2])
    return round(smoothing_coeff*init_sign,2)

def trendsure (serie):
    #Calculates a sureness by determining the length of the current trend in 
    #the smooothed curve.
    smooth = fil.KF(serie,0.03)
    i = 1
    init = np.sign(smooth[-i] - smooth[-(1+i)])
    cur = init
    while cur == init:
        i+=1
        cur = np.sign(smooth[-i] - smooth[-(1+i)])
    return i*init