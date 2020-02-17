# Smoothing Filters

import numpy as np
import math

def SMA(s, n):
    #Simple moving average
    return [0]*(n-1) + [sum([s[i] for i in range (a,a+n)])/n 
           for a in range (0,len(s)-n)]

def WMA(s, n):
    #Weighted moving average with squared weighting.
    return [s[0]]*(n-1) + [sum([(i+1-a)*s[i] for i in 
           range(a,a+n)])/(0.5*(n*(n+1))) for a in range (0,len(s)-n)]

def kalman(sys,z,x_prev,p_prev):
    #performs the kalman filter, taking as inputs the system variables, the
    #measurement, and the previous data returns as outputs the new estimate 
    #and the new error covariance
    x_pred=sys[0]*x_prev
    p_pred=sys[0]*p_prev*np.transpose(sys[0])+sys[2]
    K=(p_pred*np.transpose(sys[1]))*np.linalg.pinv((sys[1]*p_pred*
      np.transpose(sys[1]))+sys[3])
    x_new=x_pred+K*(z-sys[1]*x_pred)
    p_new=p_pred-K*sys[1]*p_pred
    return [x_new,p_new]

def kfilter (x,p,sys, data):
    # loops the filter across a dataset
    z=data[0]
    i=kalman(sys,z,x,p)
    #runs the filter once and puts the results in a varibale that the 
    #repeating loop can then use
    k=[]
    p=[]
    for l in range (len(data)):
        z=data[l]
        i=kalman(sys,z,i[0],i[1])
        k+=[np.squeeze(np.asarray(i))[0][0][0]]
        # squeezing the array version of the matrices allows for integer,
        # rather than matrix, outputs if the data being treated were non-
        # scalar, these would have to be removed
    return k

def KF (serie, coeff):
    #Full execution of the kalman filter with set smoothing coefficient.
    a=np.matrix('1,0;0,1')
    h=np.matrix('1,0;0,1')
    q=np.matrix([[coeff,0],[0,coeff]]) 
    r=np.matrix([[1-coeff,0],[0,1-coeff]])
    sys=(a,h,q,r)
    smoothed = kfilter(serie[0],1,sys,serie)
    return smoothed

def taylor(serie,n):
    #Uses taylor series to predict forward values of a smoothed series
    #UNUSED (too approximative)
    derivs = []
    newserie=serie[::-1]
    for i in range(n):
        tempserie=[newserie[j]-newserie[j+1] for j in range(len(newserie)-1)]
        derivs.append(tempserie[0])
        newserie = tempserie[::-1]
    output=[]
    x0 = serie[-1]
    for i in range(n):
        output.append(x0 + sum([(derivs[q]*(i**q))/math.factorial(q) for q 
                                in range(0,n)]))
    return output