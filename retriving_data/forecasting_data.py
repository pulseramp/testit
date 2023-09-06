
import constant
import pandas as pd 
import sys
import numpy 
import numpy as np

sys.path.append(constant.FORECASTING_DIR)
sys.path.append(constant.FORECASTING_DATA_REPO)

from logger import logging
from except_error import soft_error




class data_cleaning:
    '''
    This function is to clean the data after forecasting
    
    '''
    def __init__(self) -> None:
        pass

    

    def structure_data(self,data):
        '''
        This function will return date,present_data,forecast_data
        
        '''

        try:

            #the below will make a x-axis list 

            total_date=data[0].time_index.strftime('%Y-%m-%d').tolist()
            total_date.extend(data[2].time_index.strftime('%Y-%m-%d').tolist())

            # working for values

            present_values_=data[0].values().reshape(1,-1)[0].tolist()
            forecast_values_=data[2].values().reshape(1,-1)[0].tolist()

            #forecast_value.insert(0,present_values[-1])

            present_values=[round(i,2) for i in present_values_]
            forecast_values=[round(i,2) for i in forecast_values_]
    

            logging.info('forecasting data has been structure ')

            return total_date,present_values,forecast_values 
        
        except Exception as e:
            logging.info(soft_error(e,sys))
            raise soft_error(e,sys)

            

