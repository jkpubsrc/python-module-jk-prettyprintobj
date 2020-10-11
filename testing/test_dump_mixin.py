#!/usr/bin/python3


import collections
import datetime
from jk_prettyprintobj import *



class Test2(DumpMixin):

	def __init__(self):
		self.someStr = "abc"
		self.someInt = 123
		self.someBool = True
		self.someNone = None
		self.someFloat = 3.123
		self.someDate = datetime.datetime.now()
	#

	def _dump(self, dumper:Dumper):
		dumper.dumpVar("someStr", self.someStr)
		dumper.dumpVar("someInt", self.someInt)
		dumper.dumpVar("someBool", self.someBool)
		dumper.dumpVar("someNone", self.someNone)
		dumper.dumpVar("someFloat", self.someFloat)
		dumper.dumpVar("someDate", self.someDate)
	#

#


NC = collections.namedtuple("NC", [ "a", "b" ])



class Test(DumpMixin):

	def __init__(self):
		self.someStr = "abc"
		self.someInt = 123
		self.someBool = True
		self.someNone = None
		self.someFloat = 3.123
		self.someDate = datetime.datetime.now()
		self.someObj = Test2()
		self.someList = [
			"abc",
			123,
			datetime.datetime.now(),
			datetime.datetime.utcnow(),
			Test2(),
		]
		self.someTuple = (
			"abc",
			123,
			datetime.datetime.now(),
			datetime.datetime.utcnow(),
			Test2(),
		)
		self.someSet = set([ 1, 3, 5, 7, 9 ])
		self.someDict = {
			"abc": 123,
			"xyz": datetime.datetime.now(),
			"test": Test2(),
			None: True,
			0: 12345,
		}
		self.someFrozenSet = frozenset([ 1, 3, 5, 7, 9 ])
		self.someNamedTuple = NC("aa", "bb")
		self.someOrderedDict = collections.OrderedDict()
		self.someDefaultDict = collections.defaultdict()
		self.someDequeue = collections.deque()
	#

	def _dump(self, dumper:Dumper):
		dumper.dumpVar("someStr", self.someStr)
		dumper.dumpVar("someInt", self.someInt)
		dumper.dumpVar("someBool", self.someBool)
		dumper.dumpVar("someNone", self.someNone)
		dumper.dumpVar("someFloat", self.someFloat)
		dumper.dumpVar("someDate", self.someDate)
		dumper.dumpVar("someObj", self.someObj)
		dumper.dumpVar("someTuple", self.someTuple)
		dumper.dumpVar("someList", self.someList)
		dumper.dumpVar("someDict", self.someDict)
		dumper.dumpVar("someSet", self.someSet)
		dumper.dumpVar("someFrozenSet", self.someFrozenSet)
		dumper.dumpVar("someNamedTuple", self.someNamedTuple)
		dumper.dumpVar("someOrderedDict", self.someOrderedDict)
		dumper.dumpVar("someDefaultDict", self.someDefaultDict)
		dumper.dumpVar("someDequeue", self.someDequeue)
	#

#




t = Test()
t.dump()






































