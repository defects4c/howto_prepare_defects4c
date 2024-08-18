import sys

import re

from glob2 import glob 
import os 
import jmespath 

import json 



FINDER = r"@@\s?(?P<r1>\-\d+,\d+)\s?(?P<r2>\+\d+,\d+)\s?@@(?P<func>([^\n]*))\n"
invalid_all_add=r"@@\s\-\d+,0\s\+([\d,\s]{1,})\s@@"
is_cpp_c_file = lambda x: os.path.splitext( x)[-1] in [".cc",".c",".cpp",".c++",".cxx",".h", ".hpp" ]
HG_BIN= "/root/.local/bin/hg"
GIT_BIN= "git"
NUL_WORKERS= os.cpu_count()-1



def is_match_or_not_return_src(json_dict=None, filename_list = None  ):
    if filename_list is None:
        filename_list= jmespath.search( "files[].filename", json_dict )
    if filename_list is None :
        return False ,{}

    test_file_list=  [c for c in filename_list if is_test_filename(file_path=c)]
    if len(test_file_list)<=0:
        return False, {}
    filename_list = [c for c in filename_list if is_cpp_c_file (c) and (not is_test_filename(file_path=c) ) ]
    src_file_list = set(filename_list)-set(test_file_list)
    return len( src_file_list )==1 ,{"src": list(src_file_list), "test": test_file_list }


def is_test_filename(file_path):
    def is_test_file_path(xpath):
        d= os.path.dirname( xpath )
        if len(d)<=0:
            return False #raise Exception("unk {} , {}".format(d, file_path) )
        d = d if "/" ==d[0] else "/"+d
        return any(["/test" in d or "/tests" in d ] )
    flg = []
    flg+=[ os.path.basename(file_path) .startswith("test") ]
    flg+=[  os.path.basename(file_path) .endswith("test.c") ]
    flg+=[  os.path.basename(file_path) .endswith("test.cc") ]
    flg+=[  os.path.basename(file_path) .endswith("test.cpp") ]
    flg+=[  os.path.basename(file_path) .endswith("tests.c") ]
    flg+=[  os.path.basename(file_path) .endswith("tests.cc") ]
    flg+=[  os.path.basename(file_path) .endswith("tests.cpp") ]
    flg+=[   is_test_file_path( xpath=file_path)  ]

    return any( flg )



def parse_patch_for_hunk_line_func_tmp(patch_content  ):
    grp_list = re.findall(FINDER ,  patch_content )

    patch_info= {
        # "fn":os.path.basename(fn),
        "line_is_single":False,
        "line_number":None,

        "hunk_is_single":False,
        "hunk_start":None,
        "hunk_end":None,

        "func_is_single":False,
        "func_start_est":None,
        "func_end_est":None,
        
        "func_start_byte":None,
        "func_end_byte":None,
        "func_start_line":None,
        "func_end_line":None,

        
        }

    # def _parse_valid():
    #     re.

    def _parse_function(grp_list):
        fn_list= [x[-1] for x in grp_list]
        fn_list = set(fn_list)


        patch_info["func_is_single"]= len(fn_list)==1
        if len(fn_list)==1 :
            left_pos_1,left_offset_1 = map(abs_in, grp_list[0][0].split(",") )
            left_pos_2,left_offset_2 = map(abs_in, grp_list[-1][0].split(",") )

            patch_info["func_start_est"]= left_pos_1
            patch_info["func_end_est"]=max(0, left_pos_2+(left_offset_2-1) )


        return

    abs_in = lambda x:abs(int(x))
    def _parse_line_number( ):
        how_many = patch_content.count("\n-")


        if how_many==1 :
            patch_info["line_is_single"]=True

            left_pos,left_offset = map(abs_in, grp_list[0][0].split(",") )
            rigt_pos,rigt_offset = map(abs_in, grp_list[0][1].split(",") )
            #
            ii =0
            for _, line in enumerate( patch_content.split("\n") ):
                if line.startswith("-") and not line.startswith('+++') :
                    patch_info["line_number"]=left_pos+(ii-1)
                    ## -1 for @@....@@
                if not  line.startswith("+"):
                    ii+=1
                    
            patch_info["hunk_is_single"]=True

        return

    def _parse_hunk(grp_list ):
        new_grp_list = grp_list
        how_many = patch_content.count("\n-")

        if len(new_grp_list)==0 : ## only add in right side
            patch_info ["hunk_start"]=-1
            patch_info ["hunk_end"]=-1
            patch_info ["hunk_is_single"]=False
            return
        elif len(new_grp_list)==1 :
            a, b = map(int, new_grp_list[0][0].split(','))
            a, b = map(abs,(a,b) )
            if how_many== b-6 :
                patch_info ["hunk_is_single"]=True
                # print ( new_grp_list[0][0].split(',') ,"???")
                patch_info ["hunk_start"]=a+3
                patch_info ["hunk_end"]=a+b-3 #max(0,(b-1))
        return
    _parse_function(grp_list=grp_list)
    if not patch_info["func_is_single"] :
        return patch_info
    _parse_hunk(grp_list=grp_list)
    _parse_line_number ()

    return patch_info

if __name__=="__main__":
    
    with open("../data/save_file.txt") as f :
        data=  [json.loads(x) for x in f.readlines() if len(x.strip()) > 0 ]
    
    # data_none = [x for x in data if x is None ]
    # print ("is _null ", len(data_none ))
    valid_list= []
    valid_idx_list= []
    
    
    invalide = 0 
    for x in data :
        if  "data" not in x or x["data"] is None or  "files" not in x["data"]:
            invalide+=1 
            continue 
        
        json_data =  x["data"]
        # print ( x["data"]["files"] )
        st, xdict = is_match_or_not_return_src( json_dict=json_data  )
        if not  st :
            invalide+=1 
            continue 


        src_fn = xdict["src"][0]

        hunk = None 
        patch_hunk_list =  jmespath.search( "files[]" , json_data)
        for patch in patch_hunk_list :
            # print ( "patch.list", type(patch) , list(patch) )
            if patch["filename"] == src_fn and "patch" in patch :
                
                hunk  = patch ["patch"]
                break 


        # assert hunk is not None 
        if hunk is None :
            continue 


        hunk_info  =parse_patch_for_hunk_line_func_tmp(hunk ) 
        # hunk_info.pop("func_hunks")
        # print (hunk_info )
        # row.update(hunk_info )
        # return row 
        if not hunk_info["func_is_single"]:
            continue 

        
        # print (st, xdict)
        valid_list.append( xdict )
        valid_idx_list.append( x["idx"] )

    valid_idx_list = list(set(valid_idx_list))
    print ("raw", len(data)  , "invalid", invalide, "valid",  len(valid_list) ,"valid.idx" ,len(valid_idx_list))
    with open("../data/defects4c_cve.txt","w") as f :
        f.write( "\n".join( valid_idx_list ) )
        
    