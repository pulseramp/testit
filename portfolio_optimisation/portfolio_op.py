import sys
import constant
sys.path.append(constant.OPEN_BB_DIR)
sys.path.append(constant.OPEN_BB_TERMINAL_DIR)
from openbbterminal.openbb_terminal.sdk import openbb
import pandas as pd
from logger import logging
from except_error import soft_error


class port_optimisation:
    def __init__(self) -> None:
        pass


    def port_optimisation_begin(self,symbol_json_file,op_type):
        '''
        This function perform portfolio optimisation based on symbol input and optimisation type
        
        '''

        try:
    
            p_ = openbb.portfolio.po.load(symbol_json_file)

            weights,performance=eval(f"openbb.portfolio.po.{op_type}(portfolio_engine=p_,maxnan=0.4)")
            return weights,performance
        
        except Exception as e:
            logging.info(f'port optimisation error {e}')
            soft_error(e,sys)