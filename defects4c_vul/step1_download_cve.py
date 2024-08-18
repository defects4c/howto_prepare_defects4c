# ## downlaod from https://github.com/CVEProject/cvelist
# ## find /data3/code_dst2/CVEProject___cvelist -name '*.json'|xargs grep commit|grep "github.com"  >> ../data/step1_commit.list 
#
# import re
#
# def extract_urls(text):
#     url_pattern = r"xxx\/(?P<name>CVE[0-9-]+)\.json"# r"xxx\/(?<name>CVE[0-9-]+).json.*?(?<url>https?:\/\/\S+)"
#
#     matchs =  re.match(url_pattern, text, flags=re.IGNORECASE )
#
#     print (text)
#     if matchs :
#         print (matchs)  
#         name = matchs["name"]
#         url = matchs["url"]
#         url = url.split("\"")[0]
#         url = url.split("'")[0]
#
#         return {"name":name, "url": url }
#     return None 
#
# with open("../data/step1_commit.list") as f :
#     lines = f.readlines()
#
# for one_line in lines:
#
#     info = extract_urls(text = one_line )
#     if info is not None :
#         print (info )
#

from glob2 import glob 
import os 
import jmespath
import json 
from concurrent.futures import ThreadPoolExecutor

import random 

from convert_to_api_url import is_match_github_commit

search_dir = "/data3/code_dst2/CVEProject___cvelist/cvelist-master"

# print ("total", len(cve_list) ) 


 
 
if __name__=="__main__":  
    videos = glob( os.path.join(search_dir, "**", "*json") )
    # random.shuffle( videos )
    print ("total find  json ", len(videos) )
    # videos = videos[:10000]
    def process_file(i ): 
        if i%500==0:
            print (i) 
            
        f_name = videos[i]
        try:
            with open(f_name) as f :
                data = json.load(f)
        except :
            return None
        path_list = jmespath.search('references.reference_data[].name',data )
        if path_list is None :
            return None 
        path_list = [is_match_github_commit(x) for x in path_list ]
        path_list = [x for x in path_list if x is not None ]
        if len(path_list)==0 :
            return None 
        # print (path_list)
        cve_id = os.path.basename( f_name )
        cve_id = cve_id.split(".")[0]
        
        ret=  [ "\t".join([cve_id,x ]) for x in path_list ]
        ret = "\n".join(ret)
        return ret 
        # return [cve_id]+ path_list 



    num_workers=  os.cpu_count()-1  
    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        predictions = ex.map(process_file, range(len(videos)))
    
    
    predictions  =  list(predictions)
    predictions = [x for x in predictions if x is not None ]
    
    # total_c = [len(x)-1 for x in predictions ]
    total_c = len( predictions )# sum(total_c)
    print ( "total_c", total_c )
    # print (predictions[:20])
    # predictions = ["\n".join(x) for x in predictions ]
    with open("../data/step2_cve_urls.list", "w") as f :
        f.write( "\n".join(predictions) )
    
# load_one(f_name = "/data3/code_dst2/CVEProject___cvelist/cvelist-master/2019/1010xxx/CVE-2019-1010200.json" )
# load_one(f_name = "/data3/code_dst2/CVEProject___cvelist/cvelist-master/2008/4xxx/CVE-2008-4992.json" )

    