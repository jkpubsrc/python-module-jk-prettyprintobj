

import collections
import datetime

import jk_prettyprintobj







NOW = datetime.datetime(2026, 12, 31, 23, 59, 59)
NOW_UTC = datetime.datetime(2026, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc)



class Test2(jk_prettyprintobj.DumpMixin):

	def __init__(self):
		self.someStr = "abc"
		self.someInt = 123
		self.someBool = True
		self.someNone = None
		self.someFloat = 3.123
		self.someDate = NOW
	#

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar("someStr", self.someStr)
		ctx.dumpVar("someInt", self.someInt)
		ctx.dumpVar("someBool", self.someBool)
		ctx.dumpVar("someNone", self.someNone)
		ctx.dumpVar("someFloat", self.someFloat)
		ctx.dumpVar("someDate", self.someDate)
	#

#



NC = collections.namedtuple("NC", [ "a", "b" ])



class TestBase(object):

	def __init__(self):
		self.someStr = "abc"
		self.someInt = 123
		self.someBool = True
		self.someNone = None
		self.someFloat = 3.123
		self.someDate = NOW
		self.someObj = Test2()
		self.someList = [
			"abc",
			123,
			NOW,
			NOW_UTC,
			Test2(),
		]
		self.someTuple = (
			"abc",
			123,
			NOW,
			NOW_UTC,
			Test2(),
		)
		self.someSet = set([ 1, 3, 5, 7, 9 ])
		self.someDict = {
			"abc": 123,
			"xyz": NOW,
			"test": Test2(),
			None: True,
			0: 12345,
		}
		self.someFrozenSet = frozenset([ 1, 3, 5, 7, 9 ])
		self.someNamedTuple = NC("aa", "bb")
		self.someOrderedDict = collections.OrderedDict()
		self.someDefaultDict = collections.defaultdict()
		self.someDequeue = collections.deque()
		self.someLoremIpsum = "In amet at dapibus gravida, phasellus massa cursus lacus ridiculus elementum, nulla dictum non sociis montes, pulvinar integer maecenas id ultrices,. Arcu pellentesque sagittis condimentum fermentum justo, arcu a vel mi adipiscing primis, tristique eleifend et non, netus vitae. Lacus neque ornare gravida, tellus iaculis nam et interdum hac sollicitudin pharetra, non curabitur fames aliquam magna. Ullamcorper fusce aptent etiam lacus nam, praesent turpis ut aliquet purus, parturient pulvinar lectus fringilla, mauris nam tortor. Sed ac mus fermentum nisi."
		self.someListToShorten = [ "foo", "bar", "baz", "foobar", "foobaz", "whatever", "another", "evenmore", "andanother", ]
		self.someDictToShorten = {
			"foo": "fooValue",
			"bar": "barValue",
			"baz": "bazValue",
			"foobar": "foobarValue",
			"another": "anotherValue",
			"evenAnother": "evenAnotherValue",
		}
	#

#



