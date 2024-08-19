#apt-get install -y tar wget git

# Install the latest OpenJDK.
#apt-get install -y default-jdk


# Install autotools (Only necessary if building from git repository).
#apt-get install -y autoconf libtool

# Install other Mesos dependencies.
#apt-get -y install  libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev zlib1g-dev iputils-ping


if [ ! -f  /usr/include/xlocale.h ]; then 
	ln -s /usr/include/locale.h /usr/include/xlocale.h
	# https://github.com/agracio/electron-edge-js/issues/16
fi 	
