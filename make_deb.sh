#! /bin/sh

if [ "" = "$(which dpkg-deb)" ];
then
	echo Install dpkg-deb to build a Debian file.
	exit
fi
rm -rf deb
mkdir -v -p deb/usr/bin/geofetch deb/DEBIAN
VERSION=$(cat VERSION | head -n 1 -q | tr -d '\n')
tee deb/DEBIAN/control >/dev/null <<EOF
Package: geofetch
Version: $VERSION
Maintainer: GEOEGII555
Architecture: all
Description: geofetch lets you get some info about your system, just like neofetch. Usually it outputs only general information, but you can get more! Get started: geofetch --help
$(cat debian_req)
EOF
cp -v geofetch deb/usr/bin
cp -v geofetch.py deb/usr/bin/geofetch.d
chmod -R -v 0755 deb/DEBIAN
dpkg-deb --build deb
rm -rf deb
echo Done\!
