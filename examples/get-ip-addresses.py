#!/usr/bin/python3


import jk_utils




d = jk_utils.ip.LocalIPAddressDetector(["eth*", "wlan*"])

for x in d.getIPAddresses():
	print(x)

