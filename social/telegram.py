import snscrape.modules.telegram as sntele
import pandas as pd

import sys
from logger import logging
from except_error import soft_error
#telegram scrapper


import snscrape.modules.telegram as sntele
import pandas as pd
import re
from textblob import TextBlob
#telegram scrapper


class telegram_scrapper:
  def __init__(self):
    return None

    '''
    class to scrap public telegram channels and get context,links
    
    '''

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
    



  def scrapping_context(self,channels,max_limit:int=15):

    '''
    channel:list= 'name of channel to scrap data' 
    max_limit:int='number of information/post to retrieve'
    
      '''
    try:
      date_repo=[]
      outlinks_repo=[]
      context_repo=[]

      for channel in channels:
          try:

            for i,context in enumerate(sntele.TelegramChannelScraper(name=channel).get_items()):
              date_repo.append(context.date)
              outlinks_repo.append(context.outlinks)
              context_repo.append(context.content)
              if i>max_limit:
                break
          except:
             pass

      dict_file={
          'date':date_repo,
          'context':context_repo,
          'outlinks_repo':outlinks_repo
      }

      #creating dataframe 

      df=pd.DataFrame(dict_file)
      df['clean_context']=df['context'].apply(self.cleanText)

      df['Subjectivity'] = df['clean_context'].apply(self.getSubjectivity)

      df['Polarity'] = df['clean_context'].apply(self.getPolarity)

      df['Analysis'] = df['Polarity'].apply(self.getAnalysis)

      df.drop('context', axis=1,inplace=True)


      return df
    
    except Exception as e:
      logging.info(soft_error(e,sys))
      pass
       




  


  

    
  
