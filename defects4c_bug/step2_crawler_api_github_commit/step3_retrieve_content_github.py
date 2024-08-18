import os 
import json 
from requests.models import PreparedRequest
import msgpack 
from utils import api_github 

import gzip 
import traceback 

MSG_QNAME = "step3:q_name"

def build_url(url = 'http://example.com/search?q=question' , params = {'lang':'en','tag':'python'} ):
    req = PreparedRequest()
    req.prepare_url(url, params)
    # print(req.url)
    return req.url 

ret_info_list = []

def build_redis_key(api_data ):
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
    
    # ret_info_list = []
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
        ret_info_list.append( 
            {"url":contents_url, 
             "idx":_redis_key(big_id=idx1,  sha=sha_file)
            } )
        if sha_parent is not None :
            assert "?ref" in contents_url 
            parent_contents_url = build_url(url =contents_url , params={"ref":sha_parent} )
            ret_info_list.append( 
                {"url":parent_contents_url, 
                 "idx":_redis_key(big_id=idx1,  sha=sha_parent)
                 } 
            )

    return None 



def push_task_2_redis(c_handle , msg_list ):
    try :
        c_handle.ping()
    except :
        c_handle = api_github.init_redis_handle() 
    
    msg_list = [msg_list] if type(msg_list)!=list else msg_list 

    for msg in msg_list:
        c_handle .lpush(MSG_QNAME ,  msgpack.packb(msg)  )
    
        
if __name__=="__main__":
    
    # c_data = json.load(open("tests/redis@redis@f99467a9758e7e387de877425442de7356f4bcba"))
    #
    # meta= build_redis_key (api_data= c_data )
    # import pprint 
    #
    # pprint.pprint ( meta )
    # c_handle = api_github.init_redis_handle() 
    #
    # push_task_2_redis(c_handle=c_handle, msg= meta )
    #
    #
    import sys 
    from concurrent.futures import ThreadPoolExecutor

    num_workers = os.cpu_count()-1 

    gzi_path  =  sys.argv[-1]
    assert ".gz" in gzi_path  , gzi_path
    import pickle 
    with gzip.open( gzi_path,"rb" ) as f :
        videos= pickle.load(  f )
    
    print ("total readline ", len(videos) )
    ## 
    print ("test the first one ")
    api_data = videos[0]
    print (type(api_data), "type.api_data") 
    
    
    def process_file(i):
        if i%1000==0:
            print (i)
        api_data = videos[i]
        if api_data is None :
            return None 
        try :
            # api_data = json.loads(api_data )
            meta_list =  build_redis_key(api_data=api_data )
            return meta_list 
        except :
            # print ( api_data )
            traceback.print_exc()
    
    
    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        predictions = ex.map(process_file, range(len(videos)))
    
    print ("start expand ")
    predictions = list(predictions )
    
    
    assert len(ret_info_list)>10 , (len(ret_info_list), "ret_info_list")
    print ("init redis handle ")
    c_handle_list = [api_github.init_redis_handle() ] * num_workers
    
    
    def send_i(i):
        if i%1000==0:
            print (i)
        try :
            i_mod = i%num_workers 
            one_item = ret_info_list[i]
            c_handle = c_handle_list[i_mod]
            # assert type(chunk) == list , type(chunk )
            push_task_2_redis(c_handle=c_handle , msg_list=one_item )
        except :
            traceback.print_exc()

    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        send_list = ex.map(send_i, range(len(ret_info_list)))

    print ("start expand  send..")
    send_list= list(send_list)



