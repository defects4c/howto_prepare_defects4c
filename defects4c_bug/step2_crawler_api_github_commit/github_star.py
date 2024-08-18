import json 
import pandas as pd 
import pyarrow.parquet as pq


thresthold_star = 200 

import pprint 

def _func_top_rank_500_apigithub(rank_path):
    '''
    https://github.com/EvanLi/Github-Ranking/tree/master
    '''
    
    def _extract_repo_from_url(url):
        '''
        html_url    :    https://github.com/dfranx/SHADERed
        --> dfranx/SHADERed
        '''
        repo_name = url .split("github.com/")[-1]
        return repo_name 
    
        
    with open(rank_path) as f :
        top_rank_list_lang = json.load(f)

    ret_list = []
    for lang,top_rank_list  in top_rank_list_lang.items():
        ret_list += [
            {"private":False,
              "updated_at":x["pushed_at"],
              "repo_language":x["language"],
              "head_repo_full_name":_extract_repo_from_url(x["html_url"]),
              "stargazers_count":x["stargazers_count"] }  for x in top_rank_list] 

    df = pd.DataFrame( ret_list )
    return df 



def _func_github_star(star_path ):
    pds = pq.read_pandas( star_path , columns=None, use_threads=True).to_pandas()
    print ("bigq pds-->", pds.shape ,pds.columns )
    pds["head_repo_full_name"] = pds["head_repo_full_name"].apply( lambda x:x.replace('"',"") )
    
    # pds ["private"]= pds ["private"].astype("bool")
    pds ["updated_at"]= pds ["created_at"]
    pds ["stargazers_count"]= pds ["stargazers_count"].astype(int)
    # 
    # pds = pds[ ( pds["stargazers_count"]>thresthold_star ) & ( pds["repo_language"].isin( ["C","C++"] ) )] 
    pds = pds[  pds["repo_language"].isin( ["C","C++"] )  ] 

    pds = pds[ ["head_repo_full_name", "created_at", "stargazers_count" , "repo_language" ]  ]
    print (pds.shape ,pds.columns, "<---pds bigq",  )
    return pds 
def _func_github_star_from_apigithub(star_path ):
    # read structure 
    def cvt_api_2_item(item ):
        ret_item = {}
        if "meta" not in item or "full_name" not in  item ["meta"]:
            return None 
        ret_item ["head_repo_full_name"] = item ["meta"]["full_name"]
        ret_item ["private"] = item ["meta"]["private"]
        ret_item ["updated_at"] = item ["meta"]["updated_at"]
        ret_item ["stargazers_count"] = item ["meta"]["stargazers_count"]
        ret_item ["repo_language"] = item ["meta"]["language"]
        return ret_item 
    
    with open(star_path) as f :
        data = f.readlines() 
        data =[json.loads(x) for x in data ]
        data = [cvt_api_2_item(item=x)  for x in data ]
        data = [x for x in data if x is not None ]
        
    pds = pd.DataFrame( data )
    print ("api pds--->", pds.shape ,pds.columns , "count..." )
        
    pds["head_repo_full_name"] = pds["head_repo_full_name"].apply( lambda x:x.replace('"',"") )
    # pds ["private"]= pds ["private"].astype("bool")
    pds ["stargazers_count"]= pds ["stargazers_count"].astype(int)
    # pds.to_csv( "data/temp.csv" , index=False )
    # pds = pds[ ( pds["stargazers_count"]>thresthold_star ) & ( pds["repo_language"].isin( ["C","C++"] ) )] 
    pds = pds[  pds["repo_language"].isin( ["C","C++"] )  ] 
    print ( pds.shape ,pds.columns , "<---pds api" )
    return pds 

if __name__=="__main__":
    github_star3 = _func_top_rank_500_apigithub( rank_path = "/data3/code_dst2/commit_c_cpp_v2/data/Github-Ranking_lang_28_10_2023.json")
    repo_star3 = set( github_star3["head_repo_full_name"].tolist() )
    print ( "github_star3", github_star3["repo_language"].value_counts() )
    print  ("repo_star3", len(repo_star3) )
    
    
    
    github_star1 =  _func_github_star(star_path= "/data3/code_dst2/commit_c_cpp_v2/commit_tse/tse23/github_star.gz")
    repo_star1 = set( github_star1["head_repo_full_name"].tolist() )
    print  ("repo_star1", len(repo_star1) )
    
    github_star2 = _func_github_star_from_apigithub( star_path = "/data3/code_dst2/commit_c_cpp_v2/data/github_meta_filtered_v2.jsonl")
    repo_star2 = set( github_star2["head_repo_full_name"].tolist() )
    print  ("repo_star2", len(repo_star2) )

    
    # duplicate_github 
    duplicate_github = repo_star2.intersection(repo_star1)
    print ( "duplicate_github", len(duplicate_github ) )
    
    
    
    github_star  = pd.concat([github_star3, github_star2,github_star1])
    print (github_star.shape , "-->")
    github_star = github_star.sort_values('updated_at').drop_duplicates(['head_repo_full_name'], keep='last')

    print (github_star.shape , "-->")

    github_star .to_json("data/github_star_ccpp.jsonl",  orient="records", lines=True )
    
    
    