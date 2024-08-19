#!/bin/env bash 
### inplace_test.sh build_123 test_name123 test_result_123.xml

set -e


build_dir=$1

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

if [ ! -d  $build_dir ]; then 
	echo "exit with error for the folder not find"$build_dir
        exit 1 
fi 


################
## get test name 
################
#sha="${build_dir##*_}"
sha=$(echo "$build_dir" | cut -d '_' -f 2)


bug_meta_path="/src/projects/llvm___llvm-project/bugs_list.json"
# project meta 
if [ ! -f $bug_meta_path ]; then echo "the bugmeta not exist"$bug_meta_path ; exit 1  ; fi 

#jq ".[]|select( .commit_after==\"e66c2db7996ed0ce8cd27548a623ce62246be33b\" ) |.unittest.name"  /src/projects/llvm___llvm-project/bugs_list.json 
test_name=$( jq -r ".[] |select(.commit_after==\"$sha\")| .unittest.name | @tsv"   $bug_meta_path)


echo "test_name"$test_name 

if [ ! -f $test_name ]; then 

	echo "the test file ${test_name}not exist"
	exit 1 
fi 

(
 timeout 60s	$build_dir/bin/llvm-lit   $test_name    --xunit-xml-output=$last_arg_log_filename
)||(
 timeout 60s  	$build_dir/bin/llvm-lit   $test_name    -o=$last_arg_log_filename
)||(
 timeout 60s  	python3 $build_dir/bin/llvm-lit   $test_name    --xunit-xml-output=$last_arg_log_filename
)



set +e 


sleep 1 

#if [ -d $build_dir ]; then 
#	rm -fr  $build_dir
#fi 
