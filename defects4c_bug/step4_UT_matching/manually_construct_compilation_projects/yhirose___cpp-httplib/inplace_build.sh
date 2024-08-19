
set -e 

#CXXFLAGS="-Wno-error" ./bootstrap

if [ -z "$1" ] ;then  
        build_dir="build"
else 
        build_dir=$1
fi

mkdir -p $build_dir
#cd $build_dir

work_dir=$(pwd)


sed  -i 's/\.\/test//g' test/Makefile

#make -j $(nproc) 

#CXXFLAGS="-Wno-error" make -j $(nproc) check
#cd test  && make -j $(nproc) 

if [ -d "test" ] ; then 


        cd "test"  
        make clean
        make -j $(nproc) || true 

        #cd - 
        #echo "$PWD --->"

        cp  -r "$work_dir/test/" "$work_dir/$build_dir/" 

        #echo "pwd--->"
        #echo $PWD 

        #cd $build_dir 
        ls "$work_dir/$build_dir/"

        "$work_dir/$build_dir/test/test"  --gtest_list_tests || true


fi 


set +e
