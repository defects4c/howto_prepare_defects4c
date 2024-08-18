from glob2 import  glob
import json 
import base64
from concurrent.futures import ThreadPoolExecutor

import os
import gzip 
import pickle 

def process_file(i):
    fpx = videos[i]
    base64_key = os.path.basename( fpx) 
    base64_key = base64_key.replace(".jsonl","")
    assert len(base64_key)>4 , base64_key 
    with open( fpx,"rb" ) as jsf :
        data = base64.b64encode( jsf.read()  )
    return (base64_key, data )


num_workers = os.cpu_count()-1
search_dirs = ["data","data_2019","data_2020","data_2021","data_2022"]


for one_search in search_dirs :
    with gzip.open(f"export_{one_search}_online_extracted.jsonl.gz", "wb") as f :
        print ("open file handle")
        videos = []
        predictions = []
        _sub_file = glob( os.path.join(one_search,"online_extracted","*.json") )

        print ("total find ", one_search , "-->", len(_sub_file) )
        videos.extend( _sub_file )
        with ThreadPoolExecutor(max_workers=num_workers) as ex:
            predictions = ex.map(process_file, range(len(videos)))

        predictions = list(predictions)
        print ("the prediction list" , len(predictions) )
        pickle.dump(predictions , f)




