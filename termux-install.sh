#! /bin/sh

echo "This install script is for termux"
cp -v geofetch ~/../usr/bin
cp -v geofetch.py ~/../usr/bin
chmod +x ~/../usr/bin/geofetch
chmod +x ~/../usr/bin/geofetch.py
echo Done\!
