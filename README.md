# geofetch
This is a currently in-development tool to get info about the system.

# Install this automatically
## Debian, Ubuntu, Mint and other Debian based systems
Install script: `sudo bash debian-install.sh`

If you want to install in a chroot, specify path to it. If not, put a slash (/) - the root of the system.
# Manual install
## Debian, Ubuntu, Mint and other Debian based systems
1. Install dependencies

`$ cat debian_deps`

```
Depends: ...,
  ...
```
`$ sudo apt install <dependencies>`

2. Install the package

`$ sudo cp geofetch /usr/local/bin`

`$ sudo mkdir /usr/local/bin/geofetch`

`$ sudo cp geofetch.py /usr/local/bin/geofetch`

3. Done!

## Windows

1. Install Python 3.10 with pip

2. `X:\geofetch> python3 -m pip install -r requirements_win.txt`

3. Run geofetch: `X:\geofetch> python3 geofetch.py`
