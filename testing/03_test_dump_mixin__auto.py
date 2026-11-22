

import jk_logging
import jk_prettyprintobj

from _DumpableTestClass_TestBase import TestBase





class Test_auto(TestBase,jk_prettyprintobj.DumpMixin):

	pass

#





with jk_logging.wrapMain() as log:

	t = Test_auto()
	t.dump()

















