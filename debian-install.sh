#! /bin/bash

echo "This script is for Debian/Ubuntu/Mint and other OSes using apt"
read -p "Enter prefix (default=/): " prefix
if [ "$prefix" = "" ];
then
	echo No prefix specified, using the default value \(/\)
	prefix=/
fi
if [ $prefix != */ ];
then
	prefix=${prefix}/
fi
echo Installing to \"${prefix}\"...
apt -o Dir=$prefix update
apt -o Dir=$prefix install python3 python3-pip
umask 022
# python3 -m pip install
mkdir -v -p ${prefix}usr/local/bin/geofetch
cp -v geofetch ${prefix}usr/local/bin
cp -v geofetch.py ${prefix}usr/local/bin/geofetch
chmod +x ${prefix}usr/local/bin/geofetch
chmod +x ${prefix}usr/local/bin/geofetch.py
echo Done\!
