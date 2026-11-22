



import typing

from .dumper import DumpMixin





def dumpable_namedtuple(cls):
	return type(
		cls.__name__,
		(DumpMixin, cls),
		{
			"__module__": cls.__module__,
			"__doc__": cls.__doc__,
			"__slots__": (),
			"_dumpVarNames": lambda self: self._fields,
		},
	)
#










