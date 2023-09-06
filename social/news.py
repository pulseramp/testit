import constant
import sys
import requests
import pandas as pd

sys.path.append(constant.SOCIAL_DIR)

class news_agg:
    '''
    This class is news aggregrator
    
    '''


    def __init__(self) -> None:
        pass  
    


    def cryptopanic(self,filter:str=None,currencies:str=None):
        
        '''
        filter=(rising|hot|bullish|bearish|important|saved|lol)
        currencies='BTC','ETH',...

        '''
        
        filter=filter
        currencies=currencies

        url = 'https://cryptopanic.com/api/v1/posts/'
        params = {
            'auth_token': 'a43162f3a2c297319c0bc9f2b7deee38a2c17792',
            'currencies': currencies,
            'filter': filter,
            'limit':200
        }

        response = requests.get(url, params=params)
        data = response.json()
        df=pd.DataFrame(data)
        df['urls']=df['results'].apply(lambda x:x['url'])
        df['results']=df['results'].apply(lambda x:x['title'])

        return df.results,df.urls
