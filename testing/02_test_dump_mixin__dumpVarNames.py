

import jk_logging
import jk_prettyprintobj

from _DumpableTestClass_TestBase import TestBase





class Test_dumpVarNames(TestBase,jk_prettyprintobj.DumpMixin):

	def _dumpVarNames(self) -> list:
		return [
			"someStr",
			"someInt",
			"someBool",
			"someNone",
			"someFloat",
			"someDate",
			"someObj",
			"someTuple",
			"someList",
			"someDict",
			"someSet",
			"someFrozenSet",
			"someNamedTuple",
			"someOrderedDict",
			"someDefaultDict",
			"someDequeue",
			"someLoremIpsum:shorten",
			"someListToShorten:shorten",
			"someDictToShorten:shorten",
		]
	#

#




with jk_logging.wrapMain() as log:

	t = Test_dumpVarNames()
	t.dump()

















