


__author__ = "Jürgen Knauth"
__version__ = "0.2024.10.20"
__all__ = (
	"DumperSettings",
	"RawValue",
	"DumpMixin",
	"Dumper",
	"DumpCtx",
	"DEFAULT_DUMPER_SETTINGS",
	"pprint",
)





from .DumperSettings import DumperSettings
from .RawValue import RawValue
from .dumper import DumpMixin, Dumper, DumpCtx, DEFAULT_DUMPER_SETTINGS

from builtins import print as _print




#
# Print any value in a human readable way.
#
def pprint(something, printFunc = None):
	if printFunc is None:
		printFunc = _print
	else:
		assert callable(printFunc)

	dumper = Dumper()
	with dumper.createContext(None, "") as dumper2:
		dumper2._dumpX("", something)
	dumper.print(printFunc)
#




