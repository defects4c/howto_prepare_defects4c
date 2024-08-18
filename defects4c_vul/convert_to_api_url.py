import re 
from urllib.parse import urlparse
import os 


def clear_url(url):
    url = url.replace(",","")
    for split in ["@","#" ]: #"@" in url:
        url = url.split(split )[0]
    if "://" in url :
        url = url.split("://")[-1]
        url = "https://"+url 
    return url 

def is_match_github_commit(url,is_debug=False ):
    '''
    commit/sha_40 
    pull/[digit]/commits/sha_40
    '''
    commit_match  = r"\/?([\w|\.|-]+)\/([\w|\.|-]+)\/commit\/([0-9a-f]{5,})"
    pull_match  = r"\/?([\w|\.|-]+)\/([\w|\.|-]+)\/pull/[0-9]+/commits\/([0-9a-f]{5,})"

    raw_url = url 
    url = clear_url (url )
    
    url_info = urlparse(url )
    
    pathx = os.path.normpath( url_info.path  )

        
    v =  re.match( commit_match,  pathx ,flags=re.IGNORECASE)
    v1 = v 
    v2 = v 
    if v is None :
        v2 =  re.match( pull_match,  pathx ,flags=re.IGNORECASE)
        v= v2 
    
    if is_debug:
        print (raw_url , pathx, v1, v2  )
    if v :
        v_debug ={"grp1":v.group(1), "grp2":v.group(2), "sha":v.group(3) }
        return "https://api.github.com/repos/{}/{}/commits/{}".format(v.group(1), v.group(2), v.group(3) )
    
    return v 

    
# is_match_github_commit(url="XOOPS/XoopsCore25/commits/master")
# is_match_github_commit(url="XOOPS/XoopsCore25/pull/2588/commits/c254d308a7d3f1eac4d0b42837804cfffcba4bb2")
# is_match_github_commit(url="XOOPS/XoopsCore25/commit/c254d308a7d3f1eac4d0b42837804cfffcba4bb2")
#
# is_match_github_commit(url="XOOPS/XoopsCore25.cpp/commit/c254d308a7d3f1eac4d0b42837804cfffcba4bb2")
# is_match_github_commit(url="XOOPS/XoopsCore25_cpp/commit/c254d308a7d3f1eac4d0b42837804cfffcba4bb2")
 
    
# is_match_github_commit( url="pull/2588/commits/c254d308a7d3f1eac4d0b42837804cfffcba4bb2")
# is_match_github_commit( url="/commit/c254d308a7d3f1eac4d0b42837804cfffcba4bb2")
# is_match_github_commit( url="pull"+"s"+"/2588/commits/c254d308a7d3f1eac4d0b42837804cfffcba4bb2")
# is_match_github_commit( url="pull/2588"+"s"+"/commits/c254d308a7d3f1eac4d0b42837804cfffcba4bb2")

if __name__=="__main__": 
    import sys 
    # python convert_to_api_url.py ../data/cve_github_commits.txt  ../data/api_list.txt

    read_p = sys.argv[-2] 
    save_p = sys.argv[-1] 
    
    assert os.path.isfile( read_p ), read_p 
    assert not os.path.isfile( save_p ), save_p
     

    with open(read_p ) as f :
        data = [x.strip()  for x in  f.readlines() ] 
        
    
    invalide= 0 
    api_list=  [] 
    
    for x in data:
        v= is_match_github_commit( url = x )
        if v is  None : 
            invalide+=1 
        else :
            api_list.append( v )
        
    
    
        
    with open(save_p ,"w") as ff :
        api_list=  list(sorted (api_list ))
        ff.write( "\n".join(api_list)  )
    print ("save success ", save_p )


