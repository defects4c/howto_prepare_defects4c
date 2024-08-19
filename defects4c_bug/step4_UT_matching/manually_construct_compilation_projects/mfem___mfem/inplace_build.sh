


set -e 

export CXXFLAGS="-Wno-error" 

if [ -z "$1" ] ;then  
        build_dir="build"
else 
        build_dir=$1
fi

#mkdir -p $build_dir
#cd $build_dir



cmake -DMFEM_ENABLE_TESTING=on  -B $build_dir    
 
make  -C $build_dir -j $(nproc)
make -C $build_dir/tests -j $(nproc)

#ctest   -j $(nproc)




set +e

