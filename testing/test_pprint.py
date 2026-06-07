

import typing

# import jk_typing
# import jk_utils
import jk_logging
# import jk_json
import jk_prettyprintobj




class SomeNamedTuple(typing.NamedTuple):
	foo:str
	bar:int
#



with jk_logging.wrapMain() as log:

	# for k in dir(SomeNamedTuple):
	# 	print(f"{k} = {getattr(SomeNamedTuple, k)}")

	t1 = SomeNamedTuple("foo", 123)
	t2 = SomeNamedTuple("bar", 456)

	jk_prettyprintobj.pprint(t1)
	jk_prettyprintobj.pprint(t2)

