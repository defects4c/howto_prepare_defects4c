#!/bin/bash 

set -e 


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



cd $build_dir

echo $PWD

command_list=( $(find ./build/bin/ -type f -executable |grep -i test|awk '{print $NF }'   ) )


echo "the command line "$command_list
#command_list=("a" "./b" "./c")
specific_string="GTEST_COLOR"
# Function to check if a command's output contains a specific string
check_command_output() {
    local command_output
     rnd_log=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
     rnd_log=$rnd_log"_x.xml"
     echo $1  $rnd_log

    #command_output=$(
    echo  " $1 --gtest_output $rnd_log "
    bash -c " $1 --gtest_output=xml:$rnd_log "

    if [ -f $rnd_log ]; then 
            cat $rnd_log >> $junit_log
    fi 
}

echo "start filter "
# Filter the command list based on the specific string
filtered_list=()
for cmd in "${command_list[@]}"; do
    check_command_output "$cmd"
done




set +e

