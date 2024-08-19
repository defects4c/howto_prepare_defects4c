
if [ ! -d "external/spirv-headers" ]; then 

git clone https://github.com/KhronosGroup/SPIRV-Headers.git external/spirv-headers
git clone https://github.com/google/googletest.git          external/googletest
git clone https://github.com/google/effcee.git              external/effcee
git clone https://github.com/google/re2.git                 external/re2
git clone https://github.com/abseil/abseil-cpp.git          external/abseil_cpp

else 
	echo "exist........."
	ls external 
fi


