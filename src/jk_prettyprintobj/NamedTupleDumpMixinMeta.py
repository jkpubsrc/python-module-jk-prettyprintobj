

import typing

from .dumper import DumpMixin



def _dumpVarNames_x(self):
	return self._fields
#



#
# This meta class can be used to implement dumpable named tuples.
#
class NamedTupleDumpMixinMeta(typing.NamedTupleMeta):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	################################################################################################################################
	## Special Methods
	################################################################################################################################

	def __new__(cls, typename, bases, ns):
		if DumpMixin not in bases:
			bases = ( DumpMixin, ) + bases
		cls_obj = super().__new__(cls, typename+"_nm_base", bases, ns)
		bases = bases + (cls_obj,)
		return type(typename, bases, {
			"_dumpVarNames": _dumpVarNames_x
		})
	#

#






