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


($gm x64.optdebug   cctest  ) || \
( $gm x64.optdebug  d8 ) || \
(
	gn gen out/x64.optdebug
	ninja -C out/x64.optdebug 
) || \
(
	export PATH=$tool_dir:$PATH
	gn gen out/x64.optdebug
	ninja -C out/x64.optdebug 
)

set +e
