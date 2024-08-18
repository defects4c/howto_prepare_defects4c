import os 
import json 
from requests.models import PreparedRequest
import msgpack 
from utils import api_github 

import gzip 
import traceback 
import random 
import datetime 
import time 

import logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log_file.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)



MSG_QNAME = "step3:q_name"

tokens = open("./tokens.list").read()
tokens = tokens.strip().split("\n")
tokens = [x.strip() for x in tokens ]

random.shuffle(tokens)

num_workers = os.cpu_count()-1 

c_handle_list = [api_github.init_redis_handle()]*num_workers

def validate_token(c_handler, token ):
    time_limit = 60*60*1
    current_hour =datetime.datetime.now().hour #int(time.time()) // (3600//2)  # Get the current hour
    key = f"token:{token}:{current_hour}"  # Redis key for the token for the current hour

    # Check if the token key exists
    if c_handler.exists(key):
        # Get the usage count for the token in the current hour
        usage_count = c_handler.get(key)
        usage_count = int(usage_count ) if usage_count is not None else 0 
        if usage_count < 12000:
            # Increment the usage count for the token
            c_handler.incr(key)
            return True  # Token is valid
        else:
            return False  # Token usage limit reached
    else:
        # If the key doesn't exist, create a new key and set expiry for the end of the hour
        c_handler.setex(key, time_limit , 100)  # Set key with expiry at the end of the hour
        return True  # Token is valid


def get_token(c_handler, retry=10):
    """
    """
    for i in range(retry) :
        random.shuffle(tokens)
        for one_token in tokens:
            flg = validate_token( c_handler=c_handler, token =one_token  ) 
            if flg :
                return one_token 

        time.sleep(10)
        logger.info("wait a token")
    return random.sample(tokens,1)[-1]

def process_file(i):
    verbose = False 
    if i%1000==0:
        verbose = True 
        print (i)
        logger.info  (i)
    i_mod = i%num_workers 
    c_handler = c_handle_list[i_mod]
    
    def consumer_func(item ):
    
        def search_(key ):
            return c_handler.get(key) is None 
        
        def set_value (key, value ):
            c_handler.setnx(key, msgpack.packb(value ) )
            
        def query_( key, url, token  ):
            status_code, meta_data = api_github.get_api( api_url = url, one_token=token  )
            if status_code>-2:
                if verbose :
                    logger.info(" query status {}".format( status_code ) )
                # set 
                set_value(key=key , value=meta_data )
        
        xtoken = get_token(c_handler = c_handler )
        query_ ( key =xkey, url = xurl , token=xtoken  )
            


    while True :
        try :
            c_handler.ping () 
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            c_handler = api_github.init_redis_handle()
            c_handle_list[i_mod] = c_handler 

        if random.randint(0,1) ==1:           
            item = c_handler.lpop( MSG_QNAME )
        else:
            item = c_handler.rpop( MSG_QNAME )
        
        if item is None :
            continue 
            
        item = msgpack.unpackb(item)
        # print (item, "item...")
        xkey, xurl  = item["idx"], item ["url"]
        if c_handler.exists(xkey):
            #if verbose:
            #    logger.info(" query exist {}".format( xkey ) )
            continue 

        try :
            consumer_func(item=item)
        except:
            logger.info( traceback.format_exc() )
    
            
            
if __name__=="__main__":
    
    import sys 
    from concurrent.futures import ThreadPoolExecutor

    
    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        predictions = ex.map(process_file, range(num_workers ) )
    
    print ("start expand ")
    predictions = list(predictions )
    
    



