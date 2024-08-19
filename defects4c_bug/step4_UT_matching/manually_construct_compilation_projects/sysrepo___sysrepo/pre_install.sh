#apt-get install -y libcmocka-dev \
#libpcre2-dev  \
#libpcre3-dev  


#apt install libsystemd-dev 
  
rm -fr $OUT/deps
mkdir -p $OUT/deps
cd $OUT/deps


  git clone --branch uncrustify-0.77.1 https://github.com/uncrustify/uncrustify
  cd uncrustify
  mkdir build
  cd build
  CC=clang cmake ..
  make -j 
  make install

          
 cd $OUT/deps
          
  #git clone   --branch  v1.0-r2 https://github.com/CESNET/libyang.git
  #git clone  https://github.com/CESNET/libyang.git
  #cd libyang
 wget   https://github.com/CESNET/libyang/archive/refs/tags/v1.0.225.zip  
 unzip v1.0.225.zip 
 cd libyang-1.0.225 
  mkdir build
  cd build
  CC=clang cmake -DCMAKE_BUILD_TYPE=Debug -DENABLE_TESTS=OFF ..
  make -j 
  make install
  


  echo "======delete====="

  rm -fr  $OUT/deps 

