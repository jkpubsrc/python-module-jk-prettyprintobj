#!/usr/bin/env python3


import json

import jk_utils




print("#### GET LOCAL MAC ADDRESSES ####\n")

print(json.dumps(
	jk_utils.mac.getMACs(),
	indent="\t",
	sort_keys=True
	))

print("#### PERFORM SINGLE PING ####\n")

print(json.dumps(
	jk_utils.ping.pingSingleHost("www.google.com", 2),
	indent="\t",
	sort_keys=True
	))

print("#### PERFORM MULTIPLE PINGS ####\n")

print(json.dumps(
	jk_utils.ping.pingMultipleHosts(["www.microsoft.com", "www.google.com"], 2, False),
	indent="\t",
	sort_keys=True
	))

print()






