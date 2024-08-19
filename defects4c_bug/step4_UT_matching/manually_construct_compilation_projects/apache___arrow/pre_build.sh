


find . -name "*.cmake" -exec sed -i  "s/dl.bintray.com\/boostorg\/release\//boostorg.jfrog.io\/artifactory\/main\/release\//g" {} +

if [ -f "cmake-format.py" ]; then 
	python cmake-format.py
fi	
