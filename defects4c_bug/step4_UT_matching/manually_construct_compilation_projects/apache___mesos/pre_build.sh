

set -e 


if [ -z "$1" ] ;then  
	        build_dir="build"
else 
		build_dir=$1
fi
cd $build_dir

make disclean || make clean || echo "not not clean" 

set +e
