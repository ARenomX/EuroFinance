# Data retrieval

import pandas_datareader.data as web

def stock(stock,starts,ends):
    #Retrieves stock closing values between start and end dates
    return web.DataReader(stock, start = starts, end = ends ,
                          data_source='yahoo')['Close'].values
                          
def day(stock , day):
    #Retrieves the close of a stock on a specific day
    try:
        return (True, web.DataReader(stock, start=day, end=day ,
                          data_source='yahoo')['Close'].values[0])
    except:
        return (False, 0)