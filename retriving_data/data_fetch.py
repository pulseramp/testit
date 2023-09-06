import sys
import constant
sys.path.append(constant.OPEN_BB_DIR)
sys.path.append(constant.OPEN_BB_TERMINAL_DIR)
from openbbterminal.openbb_terminal.sdk import openbb
from except_error import soft_error
from logger import logging
import yfinance as yf
import pandas as pd
import datetime

class get_data:

    '''
    To get data of particular stocks/crypto 
    
    '''

    def __init__(self) -> None:
        pass
    
    

    def crypto_data(self,symbol,interval:int=1440,to_symbol:str='usdt',exchange:str='binance',source:str='CCXT'):

        try:
            df=openbb.crypto.load(symbol=symbol,to_symbol=to_symbol,interval=interval,exchange=exchange,source=source)
            logging.info(f'data has been fetch from crypto_data')
            return df

        except Exception as e:
            logging.info(soft_error(e,sys))
            raise soft_error(e,sys)
            
            

    def stock_data(self,symbol):
        df=yf.download(symbol,end=pd.date_range(end=datetime.datetime.today().strftime('%Y-%m-%d'), periods=100)[0])

        return df 


    def __str__(self) -> str:
        print('This func will return the data sets')



