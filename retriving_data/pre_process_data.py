import sys

sys.path.append('./')
import pandas as pd
from logger import logging
from except_error import soft_error





class pre_process:
    '''
    This class is to pre process data for
    
    '''

    def __init__(self) -> None:
        pass

    def charts_feed_social(self,dict_file):
        '''
        type can be sum/ count
        value is column name of df like volume_usd, 

        return dict file for pie chart and bar chart respectively
        
        '''
        try:

            df=pd.DataFrame(dict_file).T

            dict_final_pie_wbtc={

                
                'open-long WBTC':df[df.trade_type=='open-long WBTC'].sum()['volume_usd'],
                'open-short WBTC':df[df.trade_type=='open-short WBTC'].sum()['volume_usd'],
                'close-long WBTC':df[df.trade_type=='close-long WBTC'].sum()['volume_usd'],
                'close-short WBTC':df[df.trade_type=='close-short WBTC'].sum()['volume_usd']
                }
            
            # dict_final_bar_wbtc={
                    
            
            #     'open-long WBTC':df[df.trade_type=='open-long WBTC'].mean()['price'],
            #     'open-short WBTC':df[df.trade_type=='open-short WBTC'].mean()['price'],
            #     'close-long WBTC':df[df.trade_type=='close-long WBTC'].mean()['price'],
            #     'close-short WBTC':df[df.trade_type=='close-short WBTC'].mean()['price']

            # }
            dict_final_pie_weth={

                'open-long WETH':df[df.trade_type=='open-long WETH'].sum()['volume_usd'],
                'open-short WETH':df[df.trade_type=='open-short WETH'].sum()['volume_usd'],
                'close-long WETH':df[df.trade_type=='close-long WETH'].sum()['volume_usd'],
                'close-short WETH':df[df.trade_type=='close-short WETH'].sum()['volume_usd']
                }
            
            # dict_final_bar_weth={
            #     'open-long WETH':df[df.trade_type=='open-long WETH'].mean()['price'],
            #     'open-short WETH':df[df.trade_type=='open-short WETH'].mean()['price'],
            #     'close-long WETH':df[df.trade_type=='close-long WETH'].mean()['price'],
            #     'close-short WETH':df[df.trade_type=='close-short WETH'].mean()['price']
            # }

            
            # return dict_final_pie_wbtc,dict_final_bar_wbtc,dict_final_pie_weth,dict_final_bar_weth 
            return dict_final_pie_wbtc,dict_final_pie_weth
            

        except:
            pass
    

    def vc_raises_clean(self,path):

        df=pd.read_csv(path)

        name=df['Name'].tolist()
        date=df['Date'].tolist()
        amount=df['Amount_Raised'].tolist()
        round_no=df['Round'].tolist()
        description=df['Description'].tolist()

        

        data_dict = {
            str(index): {'name': name, 'date': date,'amount':amount,'round_no':round_no,'description':description}
            for index, (name, date,amount,round_no,description) in enumerate(zip(name, date,amount,round_no,description))
        }

        return data_dict
    

    
    def macro_clean_events(self,data):


        try:


            df=data
            print(df.columns)

            Time=df['Time(ET)'].tolist()
            Country=df['Country'].tolist()
            Event=df['Event'].tolist()
            Actual=df['Actual'].tolist()
            Consensus=df['Consensus'].tolist()
            Previous=df['Previous'].tolist()
            Date=df['Date'].tolist()
        
        

            

            data_dict = {
                str(index): {'Time': Time, 'Country': Country,'Event':Event,'Actual':Actual,'Consensus':Consensus,'Previous':Previous,'Date':Date}
                for index, (Time, Country,Event,Actual,Consensus,Previous,Date) in enumerate(zip(Time, Country,Event,Actual,Consensus,Previous,Date))
            }

            return data_dict
        
        except:
            pass
    
    def macro_clean_indices(self,data,symbol_id:list):

        '''
        This function is to clean the data of indices like CPI,URATE
        will return data and value into string form
        '''
        try:


            value=eval(f"data['United_States']{symbol_id}.to_list()")
            #converting to 2 digit decimal
            value=[round(i,2) for i in value ]
            date=eval(f"data['United_States']{symbol_id}.index.strftime('%Y-%m-%d').to_list()")
            logging.info('macro_clean_indices function has been called for class preprocess')

            return date,value
        

        except Exception as e:
            logging.info(soft_error(e,sys))
            raise soft_error(e,sys)

    
    def macro_index(self,data,symbol_id):


        try:
            date=eval(f"data{symbol_id}.keys().strftime('%D').to_list()")
            value=eval(f"data{symbol_id}.values.tolist()")
            logging.info('macro_index function has been called for class preprocess')


            return date,value
        
        except Exception as e:
            logging.info(soft_error(e,sys))
            raise soft_error(e,sys)

    def stock_index(self,data):
        pass




        
        
       
        
        
        
        
        



