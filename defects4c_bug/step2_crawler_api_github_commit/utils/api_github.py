import json 
import base64 

import sys 

import os 
import logging 
import random 
import requests 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log_file.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


import traceback
from concurrent.futures import ThreadPoolExecutor


import backoff

import numpy as np 

num_workers = os.cpu_count()-1 


tokens="""
ghp_this_is_token
"""



tokens = tokens.split("\n")
tokens = [x.strip() for x in tokens  if x.strip() !=""]
logger.info ("total token %s"%( len(tokens ) ) )


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
		requests.exceptions.ProxyError,
		requests.exceptions.SSLError,
		requests.exceptions.HTTPError,
    ),
    max_value=60,
    factor=1.5,
)
def get_api(api_url, one_token=None ):

    proxies = { 
            "http"  : "http://127.0.0.1:9100", 
            "https"  : "http://127.0.0.1:9100", 
          }
    api_url = api_url.replace('"',"")
    if one_token is None :
        x_token = random.sample(range(len(tokens)-1), 1)[-1]
        x_token = tokens[x_token]
    else :
        x_token = one_token 

    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            "authorization":f"Bearer {x_token}",
            }
    # url =  f"https://api.github.com/repos/{repo_name}?page=0&per_page=100"
    r = requests.get(api_url, headers=headers, proxies=proxies, timeout=200 )
    if r.status_code == 404 :
        return -1, None 
    elif r.status_code == 422 :
        return -1 , None 
    elif r.status_code == 403 :
        return -2 , None 
    #elif r.status_code == 503 :
    #    return -2 , None 
    elif r.status_code == 401 :
        return -2 , None 
    r.raise_for_status() 
    
    data = r.json()
    error = data.get("message", None )
    if error is not None :
        if "API rate limit" in error :
            return -2 , data 
        elif "Not Found"== error :
            return -1 ,  data 
    # star_count = data.get("stargazers_count", -3 )
    return 0 , data 


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def head(iterable, max=10):
    first = next(iterable)      # raise exception when depleted
    def head_inner():
        yield first             # yield the extracted first element
        for cnt, el in enumerate(iterable):
            yield el
            if cnt + 1 >= max:  # cnt + 1 to include first
                break
    return head_inner()


def get_api_with_batch():
    predictions = []
    
    all_videos = list(query_list_dict)
    random.shuffle(all_videos )
    random.shuffle(tokens)
    ## dispatch each token the repo 
    for  token_idx , videos in enumerate( list(chunks(all_videos,num_workers*4 ) ) ):
        if len(tokens)<=0:
            logger.info("valid tokens is null, wait moment")
            break 
        one_token = tokens[token_idx % len(tokens) ]
        print ("one_token-->" , one_token )
        
        def process_file(i):
            if i%(num_workers*2)==0:
                print (i)
            try :
                key_base64  = videos[i]
                commit_url = query_list_dict[key_base64]
                key_base64  = key_base64.decode("utf-8") if type(key_base64)==bytes else key_base64  
                status_code, git_meta = get_api( api_url =commit_url , one_token = one_token  )
                # if status_code >-2 :
                #     with open(  os.path.join(save_dir, key_base64+".json" ) , "w") as f :
                #         f.write( json.dumps( git_meta, indent=4 )  )
                return   {"api_url":key_base64, "api_data": git_meta , "status_code":status_code } 
            except :
                traceback.print_exc()
                pass 


        with ThreadPoolExecutor(max_workers=num_workers) as ex:
            predictions = ex.map(process_file, range(len(videos)))

        
        predictions = list( predictions )
        predictions = [x for x in predictions if x is not None ]
        logger.info ("finish , %s"%( str( np.unique([x["status_code"] for x in predictions ], return_counts=True ) ))  )
        status_code, count = np.unique([x["status_code"] for x in predictions ], return_counts=True )
        if set(status_code.tolist())==set([-2]):
            logger.info("fail with limit rate ")
            tokens.pop( tokens.index(one_token ) )
            print("now pop", one_token , "the len. tokens ",len(tokens),  "can index", one_token  in tokens  )
                
        
        logging.shutdown()
        sys.stdout.flush()
        sys.stderr.flush()    
                
    return predictions 


from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode

def init_redis_handle():
    nodes = [
        ClusterNode('10.96.187.173', 6379), 
        ClusterNode('10.96.187.131', 1883), 
        ClusterNode('10.96.187.189', 6379), 
        ClusterNode('10.96.187.189', 1883), 
        ClusterNode('10.96.185.201', 6379), 
        
        ClusterNode('10.96.183.224', 6379), 
        ClusterNode('10.96.183.224', 6380), 
        ClusterNode('10.96.183.224', 6381), 
        ClusterNode('10.96.183.224', 6382), 
        ClusterNode('10.96.183.224', 6383), 
        ClusterNode('10.96.183.224', 6384),
        
        ClusterNode('10.96.183.251', 6379), 
        ClusterNode('10.96.183.251', 6380), 
        # ClusterNode('10.96.183.251', 6382), 
        ClusterNode('10.96.183.251', 6383), 
        # ClusterNode('10.96.183.251', 6384), 
        
        ClusterNode("10.96.183.228",4955),

        ClusterNode('10.96.186.216', 6379), 
        ClusterNode('10.96.186.216', 6380), 
        ClusterNode('10.96.186.216', 6381), 
        ]
    rc = Redis(startup_nodes=nodes)
    return rc 




# def redis_task_q(redis_handle, q_name , msg  ):

            
            
            
            
            
