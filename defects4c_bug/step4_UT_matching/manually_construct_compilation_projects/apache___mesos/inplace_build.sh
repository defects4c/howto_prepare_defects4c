

set -e 

CXXFLAGS="-Wno-error" ./bootstrap

if [ -z "$1" ] ;then  
        build_dir="build"
else 
        build_dir=$1
fi

mkdir -p $build_dir
cd $build_dir

CXXFLAGS="-Wno-error" ../configure     --disable-python  --disable-werror   --disable-java  
#--with-boost=/usr/include/boost


make -j $(nproc) 

#CXXFLAGS="-Wno-error" make -j $(nproc) check


set +e
