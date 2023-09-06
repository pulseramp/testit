import schedule
import time
import constant
import sys
from config_it.connect_est import connect_config
from config_it.config_keys import config_value
from config_it import MONGODB_CRED_DB,MONGODB_COLL
sys.path.append(constant.DUNE_DIR)
from dune.dune_setup import dune_analytics

sys.path.append(constant.CONFIG)

def dune_gems():
    c=config_value()
    keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':'dune_gems'})
    id=keys['id']
    keys=keys['api_key']

    ## generating url from data received from mongodb
    d=dune_analytics(keys)
    url=d.make_api_url('execute',id)
    d.execute_query(url)

    print('gems script has been executed')

schedule.every(240).minutes.do(dune_gems)


def dune_vc():
    c=config_value()
    keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':'dune_vc'})
    id=keys['id']
    keys=keys['api_key']

    ## generating url from data received from mongodb
    d=dune_analytics(keys)
    url=d.make_api_url('execute',id)
    d.execute_query(url)

    print('Vc script has been executed')

schedule.every(1440).minutes.do(dune_vc)


def dune_gmx():
    c=config_value()
    keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':'dune_gmx'})
    id=keys['id']
    keys=keys['api_key']

    ## generating url from data received from mongodb
    d=dune_analytics(keys)
    url=d.make_api_url('execute',id)
    d.execute_query(url)

    print('gmx script has been executed')

schedule.every(360).minutes.do(dune_gmx)


def dune_nfts():
    c=config_value()
    keys=c.value_retrieve(MONGODB_CRED_DB,MONGODB_COLL,{'name':'dune_nfts'})
    id=keys['id']
    keys=keys['api_key']

    ## generating url from data received from mongodb
    d=dune_analytics(keys)
    url=d.make_api_url('execute',id)
    d.execute_query(url)

    print('gems script has been executed')

schedule.every(1440).minutes.do(dune_nfts)




while True:
    schedule.run_pending()
    time.sleep(1)