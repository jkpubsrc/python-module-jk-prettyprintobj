

import jk_logging
import jk_prettyprintobj

from _DumpableTestClass_TestBase import TestBase





class Test_dump(TestBase,jk_prettyprintobj.DumpMixin):

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar("someStr", self.someStr)
		ctx.dumpVar("someInt", self.someInt)
		ctx.dumpVar("someBool", self.someBool)
		ctx.dumpVar("someNone", self.someNone)
		ctx.dumpVar("someFloat", self.someFloat)
		ctx.dumpVar("someDate", self.someDate)
		ctx.dumpVar("someObj", self.someObj)
		ctx.dumpVar("someTuple", self.someTuple)
		ctx.dumpVar("someList", self.someList)
		ctx.dumpVar("someDict", self.someDict)
		ctx.dumpVar("someSet", self.someSet)
		ctx.dumpVar("someFrozenSet", self.someFrozenSet)
		ctx.dumpVar("someNamedTuple", self.someNamedTuple)
		ctx.dumpVar("someOrderedDict", self.someOrderedDict)
		ctx.dumpVar("someDefaultDict", self.someDefaultDict)
		ctx.dumpVar("someDequeue", self.someDequeue)
		ctx.dumpVar("someLoremIpsum", self.someLoremIpsum, "shorten")
		ctx.dumpVar("someListToShorten", self.someListToShorten, "shorten")
		ctx.dumpVar("someDictToShorten", self.someDictToShorten, "shorten")
	#

#




with jk_logging.wrapMain() as log:

	t = Test_dump()
	t.dump()
















