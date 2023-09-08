from django.shortcuts import render,redirect
import json
import sys
import numpy as np
import constant
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import pandas as pd

####### this lib for config of values #############
sys.path.append(constant.CONFIG)
sys.path.append(constant.OPEN_BB_DIR)
sys.path.append(constant.OPEN_BB_TERMINAL_DIR)
sys.path.append(constant.DUNE_DIR)






## this lib for dune endpoints ###############
from config_it.connect_est import connect_config
from config_it.config_keys import config_value
from config_it import MONGODB_CRED_DB,MONGODB_COLL,MONGODB_TELE_CHN,MONGODB_TELE


####### this lib for social intelligence ###############

sys.path.append(constant.SOCIAL_DIR)
from social.news import news_agg
from retriving_data.pre_process_data import pre_process
from social.twitter import twitter_analysis 


##### this lib for degens ##############
from social.telegram import telegram_scrapper




### lib for VC ###
sys.path.append(constant.DUNE_DIR)
from dune.dune_setup import dune_analytics





############### login page ##########
from config_it import MONGODB_CUST_LOG,MONGODB_CRED_CUST
from webpage.models import CustomUser

from django.shortcuts import redirect





####################login wrapper#################

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.session.get('authenticated'):
            return redirect('/pages_login',{'message':'Invalid user'})
        return view_func(request, *args, **kwargs)
    return wrapper









#####################################################  main program starts here #############################################



#####################  homepage ################################
#@cache_page(60*15)

def homepage(request):
    return render(request,'base.html')

###### error repath ######
def error_view(request):
    # Perform any necessary actions, such as logging the error or redirecting to an error page
    return redirect('/') 


#################### Macro Economics ###########################
#@cache_page(60*15)

@login_required
def macro(request):
    return redirect('/pages-error-404')

###################  social/ market intelligence ####################

@cache_page(60*15)
@login_required
def socialintelligence(request):
    return redirect('/pages-error-404')


        




###########################  Funds /Vcs ###############################

@cache_page(60*15)
@login_required
def VCs(request):   

  
   # retriving data from mongodb
    c=config_value()
    keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':'dune_vc'})
    id=keys['id']
    keys=keys['api_key']
 

 ## creating url to get response from dune 

    d=dune_analytics(keys)
    url=d.make_api_url('results',id)
    p=connect_config()
    dict_values=p.dune_endpoints(url,keys)

    data=dict_values


    # retriving data from mongodb
    c=config_value()
    keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':'dune_vc_in_out'})
    id=keys['id']
    keys=keys['api_key']
 

 ## creating url to get response from dune 

    d=dune_analytics(keys)
    url=d.make_api_url('results',id)
    p=connect_config()
    dict_values=p.dune_endpoints(url,keys)

    data_in_out=dict_values

    symbol=[]
    amount_usd=[]   

    #### preprocess for pie chart 

    for _,j in data.items():
        symbol.append(j.symbol)
        amount_usd.append(j.amount_usd)


    name_amount_dict = {}  # Dictionary to store unique names and their corresponding amounts

    # Iterate over the lists simultaneously
    for name, amount in zip(symbol, amount_usd):
        if name in name_amount_dict:
            name_amount_dict[name] += amount
        else:
            name_amount_dict[name] = amount

    name_amount_dict = dict(sorted(name_amount_dict.items(), key=lambda x: x[1], reverse=True))

    # Get the unique names and their corresponding sums as separate lists
    symbol = list(name_amount_dict.keys())
    amount_usd = list(name_amount_dict.values())



    ##### preprocess for bar chart #####
    df=pd.DataFrame(data).T
    set_name=set(df.name)
    set_name
    name_vc=[]
    amount_vc=[]
    for i in set_name:
        amount_vc.append(round(df[df.name==f'{i}'].sum()['amount_usd'],2))
        name_vc.append(i)

         

   ## vc_raises block ###

    p=pre_process()
    raises_vc=p.vc_raises_clean('./static/raises.csv')



    ##### vc /fund raise telegram intelligence #####

    c=config_value()

    tele_crypto_raise_channel=c.value_retrieve(MONGODB_TELE,MONGODB_TELE_CHN,{'name':'crypto_fundraising'})
    tele_crypto_raise_channel=tele_crypto_raise_channel['channel'].split(',')

    p=telegram_scrapper()
    content_df_raises_list=p.scrapping_context(tele_crypto_raise_channel,10).clean_context.to_list()
    content_df_raises_list=[i.replace('\u200b\u200b','') for i in content_df_raises_list]
    content_df_raises_list=[i.replace('Crypto Fundraising (StandWithUkraine 🇺🇦) pinned «','') for i in content_df_raises_list]
    content_df_raises_list=[i.replace('Crypto Fundraising (StandWithUkraine 🇺🇦) pinned a GIF','') for i in content_df_raises_list]
    content_df_raises_list_final=set(content_df_raises_list)

 

    context={
        
        'VCs':data,
        'VCs_sit':data_in_out,
        'amount':amount_usd,
        'token_symbol':symbol,
        'raises_vc':raises_vc,
        'content_df_raises_list':content_df_raises_list_final,
        'name_vc':name_vc,
        'amount_vc':amount_vc
        
        }


    return render(request,'VCs.html',context=context)

##########################  Gems ############################

@cache_page(60*15)
@login_required
def gems(request):

### dune gems #####

    c=config_value()
    keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':'dune_gems'})
    id=keys['id']
    keys=keys['api_key']

    ## generating url from data received from mongodb
    d=dune_analytics(keys)
    url=d.make_api_url('results',id)


    p=connect_config()
    dict_values_gems=p.dune_endpoints(url,keys)

##### dune smart nft holdings #######

    c_=config_value()
    keys=c_.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':'dune_nfts'})
    id=keys['id']
    keys=keys['api_key']

    ## generating url from data received from mongodb
    d=dune_analytics(keys)
    url=d.make_api_url('results',id)


    p=connect_config()
    dict_values_nfts=p.dune_endpoints(url,keys) 


    # ### pie chart for nft ###

    # data_nft=dict_values_nfts
    # pie_chart_nft_name=[]
    # pie_chart_nft_value=[]
    

    # for _,j in data_nft.items():
    #     pie_chart_nft_name.append(j.collection)
    
    # nft_collection_name=set(pie_chart_nft_name)

    # for i in nft_collection_name:
    #     pie_chart_nft_value.append(pie_chart_nft_name.count(i))

    
    # pie_chart_nft_name=list(nft_collection_name)
    
    # #pass pie_chart_nft_name ,pie_chart_nft_value
   



 
## pie chart 

    data=dict_values_gems
    pie_chart_name=[]
    pie_chart_value=[]
    

    for _,j in data.items():
        pie_chart_name.append(j.token_pair)
        pie_chart_value.append(j.amount_usd)

    name_amount_dict = {}  # Dictionary to store unique names and their corresponding amounts

    # Iterate over the lists simultaneously
    for name, value in zip(pie_chart_name, pie_chart_value):
        if name in name_amount_dict:
            name_amount_dict[name] += value
        else:
            name_amount_dict[name] = value

    name_amount_dict = dict(sorted(name_amount_dict.items(), key=lambda x: x[1], reverse=True))

    # Get the unique names and their corresponding sums as separate lists
    pie_chart_name = list(name_amount_dict.keys())
    pie_chart_value = list(name_amount_dict.values())

    ## telegram

    c=config_value()
    tele_degen_channel=c.value_retrieve(MONGODB_TELE,MONGODB_TELE_CHN,{'name':'degen'})
    tele_degen_channel=tele_degen_channel['channel'].split(',')

    p=telegram_scrapper()
    content_df_series_list=p.scrapping_context(tele_degen_channel).clean_context.to_list()
  

    name_degen,counts_degen=p.most_mentioned(content_df_series_list)


 
    context={
        'dict_values_gems':dict_values_gems,
        'dict_values_nfts':dict_values_nfts,
        'pie_chart_name':pie_chart_name,
        'pie_chart_value':pie_chart_value,
        'name_degen':name_degen,
        'counts_degen':counts_degen
 
        }



    return render(request,'gems.html',context=context)


################## forecasting page #######################

@cache_page(60*720)
@login_required
def forecasting_value(request):
    return redirect('/pages-error-404')
    

                                                    

############# portfolio optimisation ##############

@login_required
def portfolio_optimisation(request):
    return redirect('/pages-error-404')


@login_required
def fundamentals(request):

    return redirect('/pages-error-404')


@login_required
def correlation(request):

    return redirect('/pages-error-404')

##################  pages_login ##################

def pages_login(request):
    
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        c_=config_value()
        keys=c_.value_retrieve(MONGODB_CRED_CUST,MONGODB_CUST_LOG,{'username':username})
        
        
        try:
            password_check=keys['password'] 
            if password_check==password: 
                request.session['authenticated'] = True
                 
                return redirect('/gems')
            
        except:
            return render(request, 'pages_login.html',{'message':'Invalid user'})
        
    
    return render(request, 'pages_login.html') 


     


################ pages_register ####################


def pages_register(request):
    c_=config_value()
    keys=c_.value_retrieve(MONGODB_CRED_CUST,'registration',{'name':'status'})
    if keys['enabled']=='no':
        return redirect('/pages-error-404')
    
    else:


        try:

            if request.method == 'POST':
                name = request.POST.get('name')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')

                dict_inputs={
                    'name':name,
                    'email':email,
                    'username':username,
                    'password':password
                }
    
                

                d=config_value()

                d.value_input(constant.CUSTOMER_DB,constant.CUSTOMER_CRED,dict_inputs)
                return redirect('/pages_login')
            
            else:
                return render(request,'pages_register.html')
                
        except Exception as e:
            print(e)
    
#@login_required
def pages_error(request):
    return render(request,'pages-error-404.html')


#@cache_page(60*60)

def pages_contact(request): 
    if request.method == 'POST':

        name = request.POST.get('name')
        email=request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
       

        dict_inputs={
                'name':name,
                'email':email,
                'subject':subject,
                'message':message
            }
 
            

        d=config_value()

        d.value_input(constant.FEEDBACK_DB,constant.SURVEY_COLL,dict_inputs)

        return render(request,'pages-contact.html') 
    
    else:

        return render(request,'pages-contact.html') 


def logout(request):
    request.session.flush()

    return redirect('/pages_login')



     








################################# program ends here ##############################