import tweepy
# from configparser import ConfigParser
import pandas as pd
import re
from textblob import TextBlob
import config_it

from config_it.config_keys import config_value



class twitter_analysis:


    def __init__(self) -> None:
        # p=ConfigParser()
        # p.read('config.ini')

        # # Twitter API credentials
        # consumer_key = p['twitter']['API_KEYS']
        # consumer_secret = p['twitter']['API_secret_keys']
        # access_token = p['twitter']['Access_token']
        # access_token_secret = p['twitter']['Acess_token_secret']

        ## Twitter API credentials
        p=config_value()
        keys=p.value_retrieve(config_it.MONGODB_TWITTER,config_it.MONGODB_TWITTER_KEYS,{'name':'my_keys'})
        
        consumer_key = keys['consumer_key']
        consumer_secret = keys['consumer_secret']
        access_token = keys['access_token']
        access_token_secret = keys['access_token_secret'] 

        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Create API object
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    

    def twitter_user(self,username,tweet_count:int=10):

        # Define the username whose tweets you want to extract
        username = username

        # Set the number of tweets to retrieve
        tweet_count = tweet_count

        try:
            # Retrieve the user's timeline tweets
            tweets = self.api.user_timeline(screen_name=username, count=tweet_count)

            tweet_data=[]
            
            # Print the retrieved tweets
            for tweet in tweets:
                tweet_data.append(tweet.text)
            

            return tweet_data
                
            
                
        except Exception as e:
            print("Error: " + str(e))



    def twitter_search(self,topic:str='$BTC',tweet_count:int=100):

        # Define the username whose tweets you want to extract
        tweet_count=tweet_count
        topic=topic

        # creating empty list 
        text=[]
        

        try:
            tweets = self.api.search_tweets(q=topic,result_type='top',count=tweet_count)
  

            # Process and print tweets
            for tweet in tweets:
                text.append(tweet.text)

            dict_file={'context':text}



            df=pd.DataFrame(dict_file)
            df['clean_context']=df['context'].apply(self.cleanText)

            df['Subjectivity'] = df['clean_context'].apply(self.getSubjectivity)

            df['Polarity'] = df['clean_context'].apply(self.getPolarity)

            df['Analysis'] = df['Polarity'].apply(self.getAnalysis)

            df.drop('context', axis=1,inplace=True)

            return df
        
            
                
        except Exception as e:
            print("Error: " + str(e))



    def cleanText(self,text):
        if isinstance(text, str):
            text = re.sub('@[A-Za-z0-9_]+', '', text) #removes @mentions
            text = re.sub('#','',text) #removes hastag '#' symbol
            text = re.sub('RT[\s]+','',text)
            text = re.sub('https?:\/\/\S+', '', text) 
            text = re.sub('\n',' ',text)
            return text
        else:
            return ''


    ### sentiments block ###

    def getSubjectivity(self,text):
        return TextBlob(text).sentiment.subjectivity

    def getPolarity(self,text):
        return TextBlob(text).sentiment.polarity


    def getAnalysis(self,score):
        if score<0:
            return 'Negative'
        elif score ==0:
            return 'Neutral'
        else:
            return 'Positive'

    def create_wordcloud(self,text):    
        allWords = ' '.join([tweets for tweets in text])
        return allWords
        

    def most_mentioned(self,df_series):
        t=re.findall('\$[A-Za-z]+',self.create_wordcloud(df_series))
        name=[]
        counts=[]
        for i in set(t):
            name.append(i)
            counts.append(t.count(i))
        return name,counts
        


  

