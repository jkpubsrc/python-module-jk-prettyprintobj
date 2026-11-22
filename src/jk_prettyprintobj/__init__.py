


__author__ = "Jürgen Knauth"
__version__ = "0.2026.11.22"
__email__ = "pubsrc@binary-overflow.de"
__license__ = "Apache-2.0"
__copyright__ = "Copyright (c) 2020-2026, Jürgen Knauth"


__all__ = (
	"DumperSettings",
	"RawValue",
	"DumpMixin",
	"Dumper",
	"DumpCtx",
	"DEFAULT_DUMPER_SETTINGS",
	"pprint",
	"dumpable_namedtuple",
)




from .DumperSettings import DumperSettings
from .RawValue import RawValue
from .dumper import DumpMixin, Dumper, DumpCtx, DEFAULT_DUMPER_SETTINGS
from .decorators import dumpable_namedtuple

from builtins import print as _print




#
# Print any value in a human readable way.
#
def pprint(something, printFunc = None, prefix:str = ""):
	if printFunc is None:
		printFunc = _print
	else:
		assert callable(printFunc)

	assert isinstance(prefix, str)

	# ----

	dumper = Dumper()
	with dumper.createContext(None, prefix) as dumper2:
		dumper2._dumpX("", something)
	dumper.print(printFunc)
#




