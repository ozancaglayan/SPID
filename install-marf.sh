#!/bin/bash

# Download marf bundle
wget -nc -P /tmp "http://downloads.sourceforge.net/project/marf/Applications/%5Bf%5D%20SpeakerIdentApp/0.3.0-devel-20060226/SpeakerIdentApp-bundle-0.3.0-devel-20060226.tar.bz2"
mkdir -p marf &> /dev/null
tar xvf /tmp/SpeakerIdentApp-bundle-0.3.0-devel-20060226.tar.bz2 -C marf
chmod 755 marf
chown -R $USER: marf
cd marf
rm -rf html *.html retrain.lnk testing.bat
