import json 
import os 
import sys 
import gzip 
import pandas as pd 
import pyarrow.parquet as pq
import pickle 

def filter_tse_keywords( msg ):
   msg = msg .lower() 
   if ( "fix" in msg or "solve" in msg or "repair" in msg ) and (
    "bug" in msg or "issue" in msg or "problem" in msg or "error" in msg or " fault" in msg or "vulnerab" in msg  ):
       return True 
   
   return False 
    
from concurrent.futures import ThreadPoolExecutor


if __name__=="__main__":
    par_path = sys.argv[-1]
    assert os.path.isfile(par_path), par_path 
    
    assert ".jsonl" in par_path
    print (par_path )
    
    with open(par_path,"r") as f :
        videos = f.readlines()

    # videos = videos[:20000]
    print ("total data", len(videos) )
        
    def process_file(i):
        if i%1000==0:
            print (i)
        data  = videos[i]
        data = json.loads(data)
        
        msg = data["f0_"]["message"]
        
        status =  filter_tse_keywords(msg=msg  )
        
        if status :
            return json.dumps(data)
         
        return  None 

    num_workers = os.cpu_count()-1 
    
    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        predictions = ex.map(process_file, range(len(videos)))

    predictions = list(predictions) 
    predictions = [x for x in predictions if x is not None ]
    # table = pq.read_table(par_path)
    # # Optionally convert to Pandas DataFrame
    # df = table.to_pandas()
    print ("total filter data", len(predictions) )
    
    # print (df.shape, df.columns )
    new_path = par_path.replace("no_filter_","tse_filtered_")
    new_path = new_path+".gz" if  not new_path.endswith(".gz") else new_path 
    assert new_path!=par_path, (new_path, par_path )
    
    with gzip.open(new_path , "wb") as fgzip  :
        fgzip.write(  pickle.dumps(predictions)  )
    
    