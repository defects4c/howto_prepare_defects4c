import base64 
import pandas as pd 
import os 

import numpy as np 

import json 
import requests 
import pandas as pd 
import os
from concurrent.futures import ThreadPoolExecutor
import random
import gzip

import sys
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

import traceback

import time 

tokens="""
ghp_this_is_your_token
"""



tokens = tokens.split("\n")
tokens = [x.strip() for x in tokens  if x.strip() !=""]
logger.info ("total token %s"%( len(tokens ) ) )


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


num_workers = os.cpu_count()-1 

def get_star(api_url, one_token=None ):

    proxies = { 
            "http"  : "http://10.96.183.251:9100", 
            "https"  : "http://10.96.183.251:9100", 
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

#
#

from glob2 import glob 
import base64 

def base64_encode(commit_url ):
    return base64.b64encode(commit_url)

if __name__=="__main__":
    s_data_list = ["data","data_2019" , "data_2020", "data_2021", "data_2022" ]
    random.shuffle( s_data_list )
    for s_data in s_data_list :# ["data","data_2019" , "data_2020", "data_2021", "data_2022" ] :
        save_dir =f"{s_data}/online_extracted"
        os.makedirs(save_dir,exist_ok=True)

        ## load query 
        query_file_list = []
        for one_search_dir in  [ f"{s_data}/online"] :
            query_file_list += glob( os.path.join( one_search_dir, "*.jsonl" ) )
        query_list = []
        for x in query_file_list:
            query_list.extend( [json .loads(y) for y in open(x).readlines()]  )
            
        query_list_dict = {base64.b64encode(x["commit"].encode("utf-8")):x["commit"]  for x in query_list }
        logger.info ("raw total task {}".format(  len(query_list_dict) ) )
        
        ## remove exist 
        
        exist_file_list = glob( os.path.join(save_dir, "*.json" ) )
        exist_list = [ os.path.basename(x) for x in exist_file_list if os.path.isfile(x) ] 
        exist_list = [  x.replace(".json","").encode("utf-8") for x in exist_list  ] 
        logger.info ("total exist {}".format(  len(exist_list) ) )

        for exist in exist_list:
            if exist in query_list_dict:
                del query_list_dict[exist] 
        logger.info ("raw-exist total task {}".format(  len(query_list_dict) ) )
        
        ## process iteration 


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
                    status_code, git_meta = get_star( api_url =commit_url , one_token = one_token  )
                    if status_code >-2 :
                        with open(  os.path.join(save_dir, key_base64+".json" ) , "w") as f :
                            f.write( json.dumps( git_meta, indent=4 )  )
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
            # else:
            #     for item in predictions:
            #         if item ["status_code"]!=0:
            #             continue 
            #         with open(  os.path.join(save_dir, item["api_url"] ) , "w") as f :
            #             f.write( json.dumps( item["api_data"] )  )
                    
            
            logging.shutdown()
            sys.stdout.flush()
            sys.stderr.flush()    
                    
            
        logging.shutdown()
        sys.stdout.flush()
        sys.stderr.flush()    
                    
            
            
            
            
            
            
