
from pymongo import MongoClient
import os
import constant
import sys
sys.path.append(constant.CONFIG)

from config_it import MONGODB_CONNECTION_STRING
from logger import logging
from except_error import soft_error
import pandas as pd
import requests

class connect_config:

    '''
    This class is to connect to different database and server
    
    '''
    def __init__(self) -> None:
        pass


    def mongodb_config(self,database_name,collection_name):
        # Define the connection string to MongoDB

        try:
            
            connection_string = MONGODB_CONNECTION_STRING
            # Connect to MongoDB
            client = MongoClient(connection_string)

            # Select the database and collection containing the API keys
            db = client[database_name]
            collection = db[collection_name]

            logging.info(f'mongodb connection has been established')

            return collection

        except Exception as e:

            logging.info(soft_error(e,sys))
            raise soft_error(e,sys) 
        




    def dune_endpoints(self,url,keys):
        
        # Specify the API endpoint URL
        # url = "https://api.dune.com/api/v1/query/2427146/results"


        url=url


        # Specify the API query parameters
        params = {
            # "api_key":api_key,
            "api_key": keys,
            "format": "json",
        }

        # Send the HTTP request to the API endpoint
        response = requests.get(url, params=params)

        # Parse the JSON response into a DataFrame
        data = response.json()
        table = pd.DataFrame(data)
        df=pd.DataFrame(table.result.rows)
        list_value=[]
        for i in df.iterrows():
            list_value.append(i)

        dict_value=dict(list_value)

        return dict_value

# Print the table



    def aws():
        pass

   