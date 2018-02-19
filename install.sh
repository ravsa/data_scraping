#!/bin/bash

sudo yum -y install gcc gcc-c++ make flex bison gperf ruby \
  openssl-devel freetype-devel fontconfig-devel libicu-devel sqlite-devel \
  libpng-devel libjpeg-devel git nodejs npm fontconfig freetype freetype-devel fontconfig-devel libstdc++

rm -rf /tmp/phantomjs.tar.bz2
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2 -O /tmp/phantomjs.tar.bz2
mkdir -p phantomjs
tar -xjvf /tmp/phantomjs.tar.bz2 -C phantomjs --strip-components 1
./phantomjs/bin/phantomjs /phantomjs/examples/hello.js
