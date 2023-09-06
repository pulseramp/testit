from openbbterminal.openbb_terminal.sdk import openbb
import sys
import constant
from logger import logging
from except_error import soft_error

sys.path.append(constant.OPEN_BB_DIR)
sys.path.append(constant.OPEN_BB_TERMINAL_DIR)


class economy:

    def __init__(self) -> None:
        pass

    def macro_data(self, macro_id: list):
        '''
        This func will return events:dataframe , macro data:tuple
        '''
        try:

            
            df = eval(f'openbb.economy.macro({macro_id})')

            logging.info('Macro data func in economy class has been called')

            return df 

        except Exception as e:

            logging.info(soft_error(e, sys))
            raise soft_error(e, sys)


    def index(self,symbol_id:list):

        try:

            df=openbb.economy.index(symbol_id)
            logging.info('index function has been called of class economy')
            return df

        except Exception as e:
            logging.info(soft_error(e, sys))
            
        

    def events(self):
        df_events = openbb.economy.events()
        return df_events
