import os 
import pandas as pd 
import sys 
import json 

from concurrent.futures import ThreadPoolExecutor
import gzip
import pickle 

"""
python step0_group_repo.py  /data3/code_dst2/commit_c_cpp_v2/full_c_commit_list_2017_2022.jsonl
"""
thresthold = 100 ## freq >30 will clone the repo in local and 
thresthold_star  = 200  ## freq >30 will clone the repo in local and 
num_workers = os.cpu_count()-1 


def save_local_dir(save_local_dir="./data",   df_grp=None  ):
    os.makedirs(save_local_dir,exist_ok=True )
    
    uniq_repo = df_grp["repo"].unique() 
    assert len(uniq_repo)>0 , uniq_repo 
    print ( "unique len uniq_repo" , len(uniq_repo) )
    
    def each_repo(i ):
        repo_str = uniq_repo[i]
        repo_df = df_grp[ df_grp["repo"]==repo_str]
        assert len(repo_df)>0, ( len(repo_df), repo_df.shape )
        # assert len(repo_df)>thresthold, ( len(repo_df), repo_df.shape )
        repo_str = repo_str.replace("/","@")
        repo_str = os.path.join(save_local_dir, repo_str+".jsonl" )
        repo_df.to_json(repo_str, orient='records', lines=True)
        return None 
    
    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        predictions = ex.map(each_repo, range(len(uniq_repo)))
        
    predictions = list(predictions) 
    return None     
    


github_star_path = "data/github_star_ccpp.jsonl"

if __name__== "__main__":
    data_path = sys.argv[-1]
    assert len(sys.argv)>1 and os.path.isfile( data_path ) , data_path 

    year = "2017"
    # github star repo 
    github_star = pd.read_json(github_star_path  ,lines=True )
    github_star =  github_star[ github_star["stargazers_count"]>thresthold_star ]
    print ( github_star.shape, "github_star", github_star.columns )
    
    

    # data = [json.loads(x) for x in open(data_path).readlines() [:100000] ]
    if data_path.endswith(".gz"):
        with open(data_path,"rb") as gzip_f :
            data = pickle.loads(gzip_f.read())
            data = [json.loads(x) for x in data  ]
    else:
        data = [json.loads(x) for x in open(data_path).readlines() ]

    data = [{"msg":x["f0_"]["message"], "commit":x["f0_"]["url"], "created_at":x["f0_"]["created_at"] }  for x in data ]    
    
    df = pd.DataFrame(data )
    df['year'] = pd.DatetimeIndex(df['created_at']).year
    print ( df['year'].value_counts() , "year....")
    # df = df [ (df["created_at"]>"20170101")  & (df["created_at"]< "20181231") ]    
    # df = df [ (df["created_at"]>=f"{year}0101")  & (df["created_at"]<= f"{year}1231") ]    
    df = df[ df["year"]==int(year) ]
    print (df.shape,  df['year'].value_counts() , "year....")

    df["repo"] = df["commit"].apply(lambda x: x.split("com/repos/")[1] )
    df["repo"] =df["repo"] .apply( lambda x:"/".join(   x.split("/")[:2] ) ) 


    repo_lv1 = df ["repo"].tolist()
    repo_lv1 = set(repo_lv1)
    
    repo_lv2 = github_star ["head_repo_full_name"].tolist()
    repo_lv2 = set(repo_lv2)
    
    diff_repo  = repo_lv1.intersection(repo_lv2)
    print ( "repo", len(repo_lv1),  list(repo_lv1)[:20] , "start " , len(repo_lv2),  list(repo_lv2)[:20], "diff" , len(diff_repo) )
    


    print (df.shape, "commit shape...", type(github_star) )
    # print (df[:20]  )
    # print (github_star.shape )
    ### filter start 
    df = pd.merge( df, github_star, how="inner", left_on="repo" , right_on ="head_repo_full_name" )

    print ( df.shape, "--->after inner join"  )
    # print ("sort .. .")
    df['Frequency'] = df.groupby('repo')['repo'].transform('count')
    df.sort_values(['Frequency', 'repo'], inplace=True, ascending=[False, True])
    
    # print (df.shape ,"df.shape ")
    
    
    df_local  = df [ df[ "Frequency"]>thresthold   ] 
    df_online   = df [ df[ "Frequency"]<=thresthold   ] 
    
    
    
    save_local_dir(save_local_dir=f"./data_{year}/local" , df_grp=df_local )

    save_local_dir(save_local_dir=f"./data_{year}/online", df_grp=df_online )
    
    
    
