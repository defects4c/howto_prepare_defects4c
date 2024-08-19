#!/bin/env bash 

sha=$1

tool_dir=`pwd`/depot_tools
workspace_dir=`pwd`/v8
root_dir=`pwd`

set -e 

echo "now start the build "
if [ -z "$1" ] ;then  
        build_dir="build"
else 
        build_dir="build_"$sha
fi

## checkout tools
if [ ! -d ./depot_tools ]; then 
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
else
	echo "clone depot_tools (skip)"
fi 

## checkoput v8 
raw_path=$PATH
export PATH=/work/depot_tools:/work/depot_tools.git:$PATH 

if [ ! -d ./v8 ]; then 
    fetch v8 
else
	echo "fetch v8 (skip)"
fi 


cd $workspace_dir
COMMIT_DATE=$(git log -n 1 --pretty=format:%ci)

echo "================="
echo "================="
echo " sha:"$sha
echo " root_dir : "$root_dir
echo " tool_dir : "$tool_dir
echo " workspace_dir : "$workspace_dir
echo " commit date : "$COMMIT_DATE
echo "================="
echo "================="


################
###
###  src chk
###
################

cd $workspace_dir
git checkout  -f $sha
echo "check v8 version "$(git rev-parse HEAD)


################
###
###  tool chk
###
################

cd $tool_dir
echo "devtool checkout for tag "$(git log --before="$COMMIT_DATE" -n 1    --pretty=format:"%H")

git checkout -f main
git checkout -f $(git log --before="$COMMIT_DATE" -n 1    --pretty=format:"%H")

echo "the devtools head is "$(git rev-parse HEAD)
#git checkout $(git rev-list -n 1 --before="$COMMIT_DATE"  )




################
###
###  tool chk
###
################






export DEPOT_TOOLS_UPDATE=0
echo "now gclient sync for v8  ====> "
echo "cd to "$root_dir 
cd  $root_dir


#gclient sync -D  --with_branch_heads
#gclient sync -D --force --reset --with_branch_heads
echo "where_its tool-->"$(whereis gclient)

#$tool_dir/gclient sync -D --force  --with_branch_heads -v || $tool_dir/gclient sync  --force || $tool_dir/gclient sync   --with_branch_heads  

#/work/depot_tools/gclient sync -D --force  --with_branch_heads  || $tool_dir/gclient sync -D --force     --with_branch_heads  || $tool_dir/gclient sync   -D --force    
( 
	/work/depot_tools/gclient sync -D --force  --with_branch_heads 
	
) || ( 
	export PATH=`pwd`/depot_tools:$raw_path 
	$tool_dir/gclient sync -D --force     --with_branch_heads 
)  || (
	$tool_dir/gclient sync   -D --force 
)	






#######
cd $workspace_dir
gm=`pwd`/tools/dev/gm.py
echo "now check the "$gm

if [ ! -f $gm ]; then 
	mkdir -p `pwd`/tools/dev
        wget https://raw.githubusercontent.com/v8/v8/main/tools/dev/gm.py -O $gm 
        chmod +x $gm
fi 


set +e
