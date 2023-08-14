#! /usr/bin/python3

import argparse
import ctypes
import os
import socket
import psutil
import platform
import subprocess
import re

if os.name.lower() == "posix":
	import distro
if os.name == "nt":
	import wmi

# Colors
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

# Storage units
storageUnits = dict()
storageUnits["bytes"] = 1
storageUnits["KiB"] = 1024
storageUnits["MiB"] = 1024 ** 2
storageUnits["GiB"] = 1024 ** 3
storageUnits["TiB"] = 1024 ** 4

def pickStorageUnit(bytes: int) -> str:
	pickedStorageUnitName = "bytes"
	for storageUnitName in storageUnits.keys():
		storageUnitInBytes = storageUnits[storageUnitName]
		if bytes / storageUnitInBytes >= 1:
			pickedStorageUnitName = storageUnitName
	return pickedStorageUnitName

# Argument parser
parser = argparse.ArgumentParser(
	prog='geofetch',
	description='geofetch lets you get some info about your system, just like neofetch. Usually it outputs only general information, but you can get more! Get started: geofetch --help',
	epilog='The hide option has more priority than the show option'
)

# It shouldn't be that hard to get CPU info...
def get_cpu_info():
	if os.name == 'nt':
		return platform.processor()
	else:
		try:
			with open('/proc/cpuinfo', 'r') as f:
				for line in f:
					if line.strip().startswith('model name'):
						return line.split(':')[1].strip()
		except FileNotFoundError:
			pass
		try:
			output = subprocess.check_output(['getprop', 'ro.soc.manufacturer'], stderr=subprocess.DEVNULL)
			output2 = subprocess.check_output(['getprop', 'ro.soc.model'], stderr=subprocess.DEVNULL)
			return output.strip().decode('utf-8', errors='ignore') + " " + output2.strip().decode('utf-8', errors='ignore')
		except subprocess.CalledProcessError:
			pass
	return "Unknown"

def get_advertised_cpu_speed():
	if os.name == 'nt':
		# Windows Method 1
		libc = ctypes.windll.kernel32
		freq = ctypes.c_uint64(0)
		ret = libc.QueryPerformanceFrequency(ctypes.byref(freq))
		if ret:
			return f"{freq.value / 1000000:.2f} MHz"
		return "Unknown"
	# Linux Method 1
	try:
		with open('/proc/cpuinfo', 'r') as f:
			for line in f:
				if line.strip().startswith('cpu MHz'):
					return f"{float(line.split(':')[1].strip()):.2f} MHz"
	except FileNotFoundError:
		pass
	# Linux Method 2
	try:
		with open('/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq', 'r') as f:
			return f"{int(f.read()) / 1000:.2f} MHz"
	except FileNotFoundError:
		pass
	# Darwin Method 1
	libc = ctypes.CDLL(None)
	buf = ctypes.create_string_buffer(128)
	ret = libc.sysctlbyname(b'hw.cpufrequency_max', buf, ctypes.byref(ctypes.c_size_t(128)), None, 0)
	if ret == 0:
		max_freq = int.from_bytes(buf.raw, byteorder='little')
		return f"{max_freq / 1000000:.2f} MHz"
	return "Unknown"

# Setup arg parser
parser.add_argument(
	'--show-username',
	action='store_true',
	help="Show username (default)"
)
parser.add_argument(
	'--hide-username',
	action='store_true',
	help="Don't show username, overrides --show-username"
)
parser.add_argument(
	'--show-hostname',
	action='store_true',
	help="Show hostname (default)"
)
parser.add_argument(
	'--hide-hostname',
	action='store_true',
	help="Don't show hostname, overrides --show-hostname"
)
parser.add_argument(
	'--show-memusage',
	action='store_true',
	help="Show RAM and swap usage (default)"
)
parser.add_argument(
	'--hide-memusage',
	action='store_true',
	help="Don't show RAM and swap usage, overrides --show-memusage"
)
parser.add_argument(
	'--show-cpu',
	action='store_true',
	help="Show CPU usage (default)"
)
parser.add_argument(
	'--hide-cpu',
	action='store_true',
	help="Don't show CPU usage, overrides --hide-cpu"
)
parser.add_argument(
	'--show-os',
	action='store_true',
	help="Show your OS (for Linux, shows distro too) (default)"
)
parser.add_argument(
	'--hide-os',
	action='store_true',
	help="Don't show your OS (and distro on Linux), overrides --show-os"
)
parser.add_argument(
	'--show-device-info',
	action='store_true',
	help="Show your device manufacturer and model, if possible (default)"
)
parser.add_argument(
	'--hide-device-info',
	action='store_true',
	help="Don't show your device manufacturer and model, overrides --show-device-info"
)

# Parse the arguments
args = parser.parse_args()

# Variables
hostname = True
username = True
memory_usage = True
cpu = True
showOS = True
deviceInfo = True

if args.show_hostname:
	hostname = True
if args.hide_hostname:
	hostname = False
if args.show_username:
	username = True
if args.hide_username:
	username = False
if args.show_memusage:
	memory_usage = True
if args.hide_memusage:
	memory_usage = False
if args.show_cpu:
	cpu = True
if args.hide_cpu:
	cpu = False
if args.show_os:
	showOS = True
if args.hide_os:
	showOS = False
if args.show_device_info:
	deviceInfo = True
if args.hide_device_info:
	deviceInfo = False

# username@hostname

print(bcolors.OKBLUE, end="")

if hostname and not username:
	try:
		print(socket.gethostname())
	except:
		print("<unknown hostname>")
if username and not hostname:
	try:
		print(os.getlogin())
	except:
		print("<unknown user>")
if username and hostname:
	try:
		login = os.getlogin()
	except:
		login = "<unknown user>"
	try:
		host = socket.gethostname()
	except:
		host = "<unknown hostname>"
	print(f"{login}@{host}")
if username or hostname:
	print(bcolors.HEADER, end="")
	print("-" * 10)
print(bcolors.ENDC, end="")

# Memory usage

if memory_usage:
	memory = psutil.virtual_memory()
	storageUnit = storageUnits[pickStorageUnit(memory.total)]
	print(f"{bcolors.WARNING}RAM usage: {bcolors.FAIL}{round(memory.used / storageUnit, 2)}/{round(memory.total / storageUnit, 2)} {pickStorageUnit(memory.total)} ({memory.percent}%) used{bcolors.ENDC}")
	swap = psutil.swap_memory()
	storageUnit = storageUnits[pickStorageUnit(swap.total)]
	print(f"{bcolors.WARNING}Swap usage: {bcolors.FAIL}{round(swap.used / storageUnit, 2)}/{round(swap.total / storageUnit, 2)} {pickStorageUnit(swap.total)} ({swap.percent}%) used")

# CPU

if cpu:
	cpu_freq_str = f" {get_advertised_cpu_speed()} advertised speed"
	print(f"{bcolors.WARNING}CPU: {bcolors.FAIL}{get_cpu_info()} ({psutil.cpu_count()} cores){cpu_freq_str}{bcolors.ENDC}")

# OS

def is_running_on_android():
	android_files = [
		'/system/app',
		'/system/priv-app',
		'/system/vendor',
		'/system/build.prop'
	]
	return any(os.path.exists(file_path) for file_path in android_files)

def get_android_version():
	try:
		output = subprocess.check_output(['getprop', 'ro.build.version.release'], stderr=subprocess.DEVNULL)
		return output.strip().decode('utf-8', errors='ignore')
	except:
		pass
	return "unknown version"

def get_device():
	if is_running_on_android():
		output = subprocess.check_output(['getprop', 'ro.product.manufacturer'], stderr=subprocess.DEVNULL)
		output2 = subprocess.check_output(['getprop', 'ro.product.model'], stderr=subprocess.DEVNULL)
		return output.strip().decode('utf-8', errors='ignore') + " " + output2.strip().decode('utf-8', errors='ignore')
	if os.name == "nt":
		c = wmi.WMI()
		my_system = c.Win32_ComputerSystem()[0]
		return my_system.Manufacturer + " " + my_system.Model
	if os.name == "posix":
		if os.uname().sysname.lower() == "darwin":
			try:
				output = subprocess.check_output(["system_profiler", "SPHardwareDataType"], universal_newlines=True)
				manufacturer_line = [line for line in output.splitlines() if "Manufacturer" in line][0]
				model_line = [line for line in output.splitlines() if "Model Name" in line][0]
				return f"{manufacturer_line.split(':')[1].strip()} {model_line.split(':')[1].strip()}"
			except subprocess.CalledProcessError:
				pass
		else:
			try:
				output = subprocess.check_output(["dmidecode", "-s", "system-manufacturer"], universal_newlines=True)
				manufacturer = output.strip()
				output = subprocess.check_output(["dmidecode", "-s", "system-product-name"], universal_newlines=True)
				model = output.strip()
				return f"Manufacturer: {manufacturer} Model: {model}"
			except subprocess.CalledProcessError:
				pass
	return "Unknown"

if showOS:
	print(f"{bcolors.WARNING}OS kernel name and version: {bcolors.FAIL}{platform.platform()}{bcolors.ENDC}")
	if os.name.lower() == "posix":
		if is_running_on_android():
			print(f"{bcolors.WARNING}Linux distribution: {bcolors.FAIL}Android {get_android_version()}{bcolors.ENDC}")
		elif os.uname().sysname.lower() != "darwin":
			print(f"{bcolors.WARNING}Linux distribution: {bcolors.FAIL}{distro.name()} {distro.version()}{bcolors.ENDC}")

# Device
if deviceInfo:
	print(f"{bcolors.WARNING}Device: {bcolors.FAIL}{get_device()}{bcolors.ENDC}")
