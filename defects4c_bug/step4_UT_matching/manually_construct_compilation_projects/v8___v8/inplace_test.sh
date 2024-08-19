#!/bin/env bash 

set -e 

tool_dir=`pwd`/depot_tools
workspace_dir=`pwd`/v8
root_dir=`pwd`



if [ ! -d $workspace_dir ]; then 
	echo $workspace_dir" is empty  exit error"
	exit 1 
fi 

cd $workspace_dir

gm=`pwd`/tools/dev/gm.py
export PATH=/work/depot_tools/:$PATH

if [ ! -f $gm ]; then 
        wget https://raw.githubusercontent.com/v8/v8/main/tools/dev/gm.py -O $gm 
        chmod +x $gm
fi 


if [ -z $1 ]; then 
	test_name="mjsunit"
else
	test_name=$1  
fi 	

#$gm x64.optdebug   cctest 

#/usr/bin/python2 tools/run-tests.py --outdir=out/x64.optdebug  mjsunit/whitespaces2  mjsunit/whitespaces3  -vv 

####################
####################
###  expect bash inplace_test.sh xx/xx.js xxx/xxx.cc /tmp/save.log 
###  chk the input 
####################
####################

last_arg_log_filename="${!#}"

substring_list=(".txt" ".log" ".json" ".xml")

found=false
echo "check the last input is a filename or not "
for substring in "${substring_list[@]}"; do
    if [[ $last_arg_log_filename == *"$substring"* ]]; then
        found=true
        echo "Substring '$substring' is contained in the main string"
        # If you only want to find the first match, you can break out of the loop here.
        break
    fi
done

if [ "$found" = false ]; then
    echo "your save logfile ${last_arg_log_filename} are contained in "$substring_list
    exit 1 
fi


## if fail 

##  x.py name1 name2  -vv  --json-test-results=
##  x.py name1 name2    --json-test-results=
##  x.py  mjsunit  --json-test-results=
##  x.py  mjsunit 
 
#/usr/bin/python2 tools/run-tests.py --outdir=out/x64.optdebug  $test_name $2 $3 $4  -vv   --json-test-results=$last_arg_log_filename || /usr/bin/python2 tools/run-tests.py --outdir=out/x64.optdebug   mjsunit -vv  --json-test-results=$last_arg_log_filename ||  /usr/bin/python2 tools/run-tests.py --outdir=out/x64.optdebug   mjsunit    --json-test-results=$last_arg_log_filename   ||  /usr/bin/python2 tools/run-tests.py --outdir=out/x64.optdebug   mjsunit 


set +e 

#/usr/bin/
python2 tools/run-tests.py --outdir=out/x64.optdebug  $test_name $2 $3 $4  -vv   --json-test-results=$last_arg_log_filename 



#if  [ ! -e "$last_arg_log_filename" ] || 
if [ ! -s "$last_arg_log_filename" ] ; then 
	echo "1"
	#/usr/bin
	python2 tools/run-tests.py --outdir=out/x64.optdebug  $test_name $2 $3 $4    --json-test-results=$last_arg_log_filename 
fi


#if  [ ! -e "$last_arg_log_filename" ] || [ ! -s "$last_arg_log_filename" ] ; then 
if [ ! -s "$last_arg_log_filename" ] ; then 
	echo "3"
	 #/usr/bin/
	 python2 tools/run-tests.py --outdir=out/x64.optdebug   mjsunit    --json-test-results=$last_arg_log_filename
fi 	

#if  [ ! -e "$last_arg_log_filename" ] || [ ! -s "$last_arg_log_filename" ] ; then 
if [ ! -s "$last_arg_log_filename" ] ; then 
	echo "4"
	 #/usr/bin/
	 python2 tools/run-tests.py --outdir=out/x64.optdebug   mjsunit    >> $last_arg_log_filename
fi 	


#set +e
