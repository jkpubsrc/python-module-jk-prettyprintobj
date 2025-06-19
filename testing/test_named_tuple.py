

import os
import typing

import jk_typing
import jk_utils
import jk_logging
import jk_json
import jk_prettyprintobj




class SomeNamedTuple(metaclass=jk_prettyprintobj.NamedTupleDumpMixinMeta):
	foo:str
	bar:int
#



with jk_logging.wrapMain() as log:

	# for k in dir(SomeNamedTuple):
	# 	print(f"{k} = {getattr(SomeNamedTuple, k)}")

	t = SomeNamedTuple("foo", 123)
	t.dump()


