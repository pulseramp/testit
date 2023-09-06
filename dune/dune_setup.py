import requests
import sys
sys.path.append('./')
BASE_URL = "https://api.dune.com/api/v1/"

from requests import get, post
import pandas as pd



class dune_analytics:

    def __init__(self,api_key) -> None:
        self.API_KEY = api_key
        self.HEADER = {"x-dune-api-key" : self.API_KEY}
        


    def make_api_url(self,action,ID,module:str='query'):
        """
        We shall use this function to generate a URL to call the API.
        ID: query id like 819391
        action: 'results' to fetch data and 'execute' to run the query 
        module: query 
        """

        url = BASE_URL + module + "/" + ID + "/" + action

        return url

    def execute_query(self,url, engine="medium"):
        """
        Takes in the query ID and engine size.
        Specifying the engine size will change how quickly your query runs. 
        The default is "medium" which spends 10 credits, while "large" spends 20 credits.
        Calls the API to execute the query.
        Returns the execution ID of the instance which is executing the query.

        """

        url =url
        params = {
            "performance": engine,
        }
        response = post(url, headers=self.HEADER, params=params)
        last_executed = response.json()
        #last_executed=last_executed['execution_ended_at'].split('.')[0]

        return last_executed


# def get_query_status(self,execution_id):
#     """
#     Takes in an execution ID.
#     Fetches the status of query execution using the API
#     Returns the status response object
#     """

#     url = make_api_url("execution", "status", execution_id)
#     response = get(url, headers=self.HEADER)

#     return response


# def get_query_results(execution_id):
#     """
#     Takes in an execution ID.
#     Fetches the results returned from the query using the API
#     Returns the results response object
#     """

#     url = make_api_url("execution", "results", execution_id)
#     response = get(url, headers=self.HEADER)

#     return response


# def cancel_query_execution(execution_id):
#     """
#     Takes in an execution ID.
#     Cancels the ongoing execution of the query.
#     Returns the response object.
#     """

#     url = make_api_url("execution", "cancel", execution_id)
#     response = get(url, headers=self.HEADER)

#     return response
