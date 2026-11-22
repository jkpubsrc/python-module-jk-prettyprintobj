

import typing

# import jk_typing
# import jk_utils
import jk_logging
# import jk_json
import jk_prettyprintobj





@jk_prettyprintobj.dumpable_namedtuple
class SomeNamedTuple(typing.NamedTuple):
	foo:str
	bar:int
#




with jk_logging.wrapMain() as log:


	t = SomeNamedTuple("foo", 123)
	print(t.dump)
	t.dump()




