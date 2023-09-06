import sys
import constant
sys.path.append(constant.OPEN_BB_DIR)
sys.path.append(constant.RETRIVING_DATA)
sys.path.append(constant.OPEN_BB_TERMINAL_DIR)

from logger import logging
from except_error import soft_error

from openbbterminal.openbb_terminal.sdk import openbb
from retriving_data.data_fetch import get_data





class forecasting:

    def __init__(self) -> None:
        pass
    

    def forecast_crypto(self,symbol,exchange,to_symbol:str='usdt',interval:int=1440,target_column:str='Close',n_predict:int=20,forcast_type:str='rnn'):
        try:

        

            data=get_data()
            data=data.crypto_data(symbol=symbol,interval=interval,to_symbol=to_symbol,exchange=exchange)


            command=f"openbb.forecast.{forcast_type}(data=data,target_column='Close',n_predict=n_predict,n_epochs=50)"
           
            result=eval(command) 
    
            logging.info(f'forecasting process has been completed') 

            return result
        
        except Exception as e:
            logging.info(soft_error(e,sys))
            print(soft_error(e,sys))
            return None
            

    def forecast_stocks(self):
        pass



        




