import os 
import json 
from requests.models import PreparedRequest
import msgpack 
from utils import api_github 

import gzip 
import traceback 

import sys 

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode
from concurrent.futures import ThreadPoolExecutor

num_workers =  os.cpu_count()-1 

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
    rc = Redis(startup_nodes=nodes, decode_responses=False )
    return rc 
logger.info ("start init redis ")

c_handle_list = [api_github.init_redis_handle()]*num_workers
logger.info ("done init redis ")


def build_url(url = 'http://example.com/search?q=question' , params = {'lang':'en','tag':'python'} ):
    req = PreparedRequest()
    req.prepare_url(url, params)
    # print(req.url)
    return req.url 


def build_redis_key(c_handler, api_data ):
    if api_data is None :
        return None
     
    url = api_data["url"]
    
    idx1 =  url.split("api.github.com/repos/")[-1]
    # cur/ = {"idx":idx1, "sha":api_data["sha"] }

    idx_parent,sha_parent = None , None 
    parents = api_data["parents"]
    # assert len(parents)<=1 , (parents,api_data)
    if len(parents):
        url_p = parents[0]["url"]
        idx_parent =  url_p.split("api.github.com/repos/")[-1]
        sha_parent  =parents[0]["sha"]
        # parent = {"idx":id1_lvl1, "sha":parents[0]["sha"] }
    
    def _redis_key (big_id , sha ):
        idx = "{}@@{}".format(big_id, sha  )
        # idx = os.path.join(  big_id , sha )
        idx = idx .replace("/","@")
        return idx 

    def get_value_from_redis(c_handler, k ):
        data = c_handler.get(k)
        
        data = msgpack.unpackb( data ) if data is not None else None 
        
        return data

    
    ret_info_list = []
    file_list = api_data["files"]
    for one_file in file_list : 
        
        ret_info = {"cur":None,  "parent":None }
        contents_url = one_file["contents_url"]
        sha_file   = one_file["sha"]
        sha_file2   = one_file["filename"]
        sha_file = sha_file if sha_file is not None else sha_file2
        if sha_file is None or idx1 is None :
            print (  one_file )
        # cur 
        meta_info =     {
            "message": api_data.get("commit",{}).get("message",None),
            "stats": api_data.get("stats",None ), 
            "files": one_file,
            "url":contents_url, 
            "idx":_redis_key(big_id=idx1,  sha=sha_file)
            }
         
        if sha_parent is not None :
            assert "?ref" in contents_url 
            parent_contents_url = build_url(url =contents_url , params={"ref":sha_parent} )
            meta_info.update({
                "url_parent":parent_contents_url, 
                "idx_parent":_redis_key(big_id=idx1,  sha=sha_parent)
                } 
            )
            
            idx_value   = get_value_from_redis(
                c_handler=c_handler, 
                k=meta_info["idx"], 
                )
            if idx_value is None:
                idx_value   = get_value_from_redis(
                    c_handler=c_handler, 
                    k=meta_info["idx"], 
                    )
                
            idx_parent_value = get_value_from_redis(
                c_handler=c_handler, 
                k= meta_info["idx_parent"] 
            )
            
            if  idx_parent_value is None :
                idx_parent_value = get_value_from_redis(
                    c_handler=c_handler, 
                    k= meta_info["idx_parent"] 
                )
                
            
            meta_info.update({
                "idx_obj":idx_value, 
                "idx_parent_obj":idx_parent_value , 
                } 
            )
            ret_info_list.append(  meta_info )
        
            
        
        
    return ret_info_list 


def process_file(i):
    # verbose = False 
    # if i%1000==0:
    #     verbose = True 
    #     print (i)
    #     logger.info  (i)
    i_mod = i%num_workers 
    c_handler = c_handle_list[i_mod]
        
    api_data = videos [i]
    api_key , api_data = api_data 
    meta_list = None 
    try :
        api_data = base64.b64decode( api_data ) if api_data is not None else api_data 
        api_data  = json.loads( api_data ) if api_data is not None else api_data 

        meta_list = build_redis_key(c_handler=c_handler, api_data=api_data )

        # meta_list = list(itertools.chain(*meta_list))  if meta_list is not None and len(meta_list) else None 

        meta_list = json.dumps(meta_list) if meta_list is not None and len(meta_list) else None 
        
    except :
        traceback.print_exc()
        # print ( api_data )
        return None 
    
    
    return meta_list 


    


'''

# 
python step4_build_pair.py  export_data_2017_online_extracted.jsonl.gz

 
'''
import gzip 
import pickle 
import msgpack 
import base64
from functools import reduce

import itertools

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]



if __name__=="__main__":
    save_dir = "/data3/code_dst2/code_step4"
    os.makedirs (save_dir,exist_ok=True )
    
    search_dir = "/home/j/crawler_github/process_github_commit"

    online_filter_file = sys.argv[-1]
    zip_file = os.path.join(search_dir , online_filter_file )
    
    with gzip.open(zip_file, "rb") as fff :
        videos_all = pickle.load(fff )

    
    chunk_size = 10000 
    logger.info ( "data_list {} chunk number {} ".format(  len(videos_all), len(videos_all)//chunk_size ) )
    
    ii=0
    for videos in chunks( videos_all , chunk_size ):
        ii+=1
        send_list = []
        with ThreadPoolExecutor(max_workers=num_workers) as ex:
            send_list = ex.map(process_file, range(len(videos)))
    
        logger.info ("start expand  send..")
        send_list= list(send_list)
        logger.info ("total find {} ".format( len(send_list) ) )
        send_list=  [x for x in send_list if x is not None ]
        logger.info ("total find (not none) {}".format( len(send_list) ) )
    
        new_zip_file = os.path.basename(zip_file).replace("export_","pair_")
        new_zip_file = new_zip_file.replace(".gz",f"__{ii}.gz")
        assert os.path.basename(new_zip_file) !=  os.path.basename(zip_file)  , (zip_file , new_zip_file )
        
        logger.info ("save...{} .. {} ".format( new_zip_file , os.path.join(save_dir, new_zip_file ) ) )
        
        with gzip.open( os.path.join(save_dir, new_zip_file ) ,"wb") as xxxfff :
            pickle.dump( send_list, xxxfff  )

        logging.shutdown()
        sys.stdout.flush()
        sys.stderr.flush()    

