import os 
from glob2 import glob 
import json 
import pickle 

import gzip 
import base64 

from concurrent.futures import ThreadPoolExecutor

import pandas as pd 

def is_filename_ccpp(filename, 
                     ext_list= [
                            ".c",
                            ".cc",
                            ".cpp",
                            ".cxx",
                            ".c++",
                            ".h" ,
                            ".hpp" ,
                            ".cu", 
                            ]):
    
    _, file_extension = os.path.splitext(filename)
    file_extension = file_extension.lower() 
    return file_extension in ext_list 


if __name__=="__main__":
    ## for the maxsize of one file, i.e. one chunk 
    # chunk_size =  100000
    path = "export_data_2020_online_extracted.jsonl.gz"
    for path in [
        "export_data_2017_online_extracted.jsonl.gz",
        "export_data_2018_online_extracted.jsonl.gz",
        "export_data_2019_online_extracted.jsonl.gz",
        "export_data_2020_online_extracted.jsonl.gz",
        "export_data_2021_online_extracted.jsonl.gz",
        "export_data_2022_online_extracted.jsonl.gz",
        ]:
    
        with gzip.open(path,"rb")  as f :
            videos   = pickle.load( f  )
        print ("total load list" , len(videos) )
        
        # videos = videos[:10000]
        
        num_workers = os.cpu_count()-1 
    
        def process_file ( i ):
            if i%500==0:
                print (i)
                
            data  = videos [i]
            if data is None :
                return None 
            base64_key  , api_data  = data 
            api_data = base64.b64decode( api_data )
            api_raw_data  = json.loads( api_data )
            if api_raw_data is None :
                return None 
            if "sha" not in api_raw_data :
                return None 
        
            ## id --> sha 
            ## url --> api_url mapping to base64 
            ## parent commit 
            ## current commit 
            ## commit  --  message 
            # file list 
                # file meta but filter by filename extension  
            ret_item = {
                "sha": api_raw_data["sha"],
                "url": api_raw_data["url"],
                "commit":{"message":api_raw_data["commit"].get("message", None )},
                "parents":api_raw_data["parents"],
                }
            
            files =api_raw_data.get("files", [])
            files = [x for x in files if is_filename_ccpp( x["filename"])  ]
            
            if len(files)>0 :
                ret_item ["files"] = files 
            else :
                return None 
            
            return ret_item 
        
        with ThreadPoolExecutor(max_workers=num_workers) as ex:
            predictions = ex.map(process_file, range(len(videos)))
    
    
        predictions = list(predictions )
        
        predictions = [x for x in predictions if x is not None ]
        
        os.makedirs("data_filtered", exist_ok=True)
        with open(os.path.join("data_filtered/", path.replace("export_","state_filtered_").replace(".gz",".txt")) , "w") as f :
            predictions_filelist = [len(x["files"]) for x in predictions ] 
            stat_df =  pd.DataFrame( {"sta":predictions_filelist } )
            print ( stat_df["sta"].describe().to_json() )
            f.write(  stat_df["sta"].describe().to_json()  )
            
        with gzip.open(os.path.join("data_filtered/", path.replace("export_","filtered_") ), "wb") as fzip :
            print ("the prediction list" , len(predictions) )
            pickle.dump(predictions , fzip)
            
            
            
        
    