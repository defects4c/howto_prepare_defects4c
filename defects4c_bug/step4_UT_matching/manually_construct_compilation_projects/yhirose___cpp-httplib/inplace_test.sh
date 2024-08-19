
#!/bin/bash 

#set -e 


if [ -z "$1" ] ;then  
        build_dir="build"
else 
        build_dir=$1
fi


if [ -z "$1" ] ;then  
        junit_log="junit.xml"
else 
        junit_log=$2
fi



if [ ! -f "gtest_parallel.py" ]; then 
	wget "https://raw.githubusercontent.com/google/gtest-parallel/master/gtest_parallel.py"
fi	


cp gtest_parallel.py $build_dir/

cd $build_dir


#echo $PWD

command_list=( $(find ./ -type f -executable |grep -i test|awk '{print $NF }'   ) )


echo "the command line "$command_list
#command_list=("a" "./b" "./c")
specific_string="GTEST_COLOR"
# Function to check if a command's output contains a specific string
check_command_output() {
    local command_output
     rnd_log=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
     rnd_log=$rnd_log"_x.json"
     #echo $1  $rnd_log

    #command_output=$(
    #echo  " $1 --gtest_output $rnd_log "
    python gtest_parallel.py $1 --dump_json_test_results $rnd_log --timeout 100
    #bash -c " $1 --gtest_output=xml:$rnd_log "
    #echo "junit_log---> $junit_log --> rnd_log $rnd_log "

    if [ -f $rnd_log ]; then 
            cat $rnd_log >> $junit_log
	    echo "\n" >> $junit_log
	    rm $rnd_log
    fi 
}

echo "start filter "
# Filter the command list based on the specific string
filtered_list=()
for cmd in "${command_list[@]}"; do
    check_command_output "$cmd"
done




#set +e


