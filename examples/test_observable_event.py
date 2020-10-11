#!/usr/bin/env python3



from jk_utils import ObservableEvent




def myPrinter1(a):
	print("1>> " + str(a))
#

def myPrinter2(**kwargs):
	print("2>> " + str(kwargs))
#

evt = ObservableEvent("OnChangedEvent")

evt += myPrinter1
evt += myPrinter2
print(evt)

evt(a = "x")



