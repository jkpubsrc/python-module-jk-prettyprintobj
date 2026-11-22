

import typing

# import jk_typing
# import jk_utils
# import jk_logging
# import jk_json
# import jk_prettyprintobj






class _Reflection(object):

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

	@staticmethod
	def isNamedTupleInstance(obj) -> bool:
		return isinstance(obj, tuple) \
			and hasattr(type(obj), "_fields") \
			and isinstance(type(obj)._fields, tuple)
	#

	@staticmethod
	def getDumpVarNames(obj) -> list[str]:
		# retrieve instance variables
		varNames:list[str] = sorted(
			name for name in vars(obj)
				if not name.startswith("_")
		)

		# retrieve properties
		propertyNames:list[str] = []
		for cls in reversed(type(obj).__mro__):
			if cls is object:
				continue

			for name, value in vars(cls).items():
				if name.startswith("_"):
					continue

				if isinstance(value, property):
					if name not in propertyNames:
						propertyNames.append(name)

		# remove properties from instance variables
		varNames = [
			name for name in varNames
				if name not in propertyNames
		]

		# return result
		return varNames + propertyNames
	#

#

