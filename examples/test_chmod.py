#!/usr/bin/python3


import os

from jk_utils import ChModValue




print(ChModValue())



if os.path.isdir("test_chmod"):
	os.rmdir("test_chmod")
os.mkdir("test_chmod")



dstat = os.stat("test_chmod")
stat = ChModValue(dstat.st_mode)
print(stat)
stat.otherX = False
stat.groupX = False
print(stat)

stat.modify("go-r")
stat.modify("a-x")
stat.modify("ug+rw")
stat.modify("o+r")
stat.modify("a+x,o-r,o-x,g-w")
print(stat)

os.chmod("test_chmod", stat)










