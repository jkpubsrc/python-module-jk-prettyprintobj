

import collections
#import datetime






class DumperSettings(object):

	def __init__(self):
		self.showPrimitivesWithType = False
		self.showDictKeysWithType = False
		self.showComplexStructsWithType = False
		self.compactSequencLimit = 8
	#

#

DEFAULT_DUMPER_SETTINGS = DumperSettings()




def _shortenText(text:str) -> str:
	if text is None:
		return None
	if len(text) > 40:
		return text[:40] + "..."
	else:
		return text

#




POST_PROCESSORS = {
	"shorten": _shortenText
}




class _Omitted:
	pass
#

_OMITTED = _Omitted()





class DumpCtx(object):

	_TYPE_MAP = {}

	def __init__(self, s:DumperSettings, outputLines:list, exitAppend:str, prefix:str):
		self.__s = s
		self.outputLines = outputLines
		self.__exitAppend = exitAppend
		self.prefix = prefix
	#

	################################################################################################################################
	#### Methods that should be called by implementors
	################################################################################################################################

	def dumpVar(self, varName:str, value, postProcessorName:str = None):
		self._dumpX(varName + " = ", value, postProcessorName)
	#

	def dumpVars(self, caller, *args):
		if len(args) == 0:
			if hasattr(caller, "_dumpVarNames"):
				varNames = caller._dumpVarNames()
				assert isinstance(varNames, (list, tuple))
			else:
				raise Exception("Specify either variable names or a list of variables to dump!")

		elif len(args) == 1:
			if isinstance(args[0], str):
				varNames = args
			elif isinstance(args[0], (tuple, list)):
				varNames = args[0]
			else:
				raise Exception("Unexpected data in args: " + repr(args))

		else:
			varNames = args

		for varName in varNames:
			assert isinstance(varName, str)

			postProcessorName = None
			pos = varName.find(":")
			if pos == 0:
				raise Exception()
			elif pos > 0:
				postProcessorName = varName[pos+1:]
				varName = varName[:pos]

			value = getattr(caller, varName)
			self._dumpX(varName + " = ", value, postProcessorName)
	#

	################################################################################################################################
	#### Dispatcher method
	################################################################################################################################

	#
	# This method outputs a value (recursively).
	# To achieve this this method analyses the data type of the specified value and invokes individual type processing methods if available.
	#
	def _dumpX(self, extraPrefix:str, value, postProcessorName:str = None):
		if value is None:
			self._dumpPrimitive(extraPrefix, value, postProcessorName)
			return

		t = type(value)
		m = DumpCtx._TYPE_MAP.get(t)
		if m:
			m(self, extraPrefix, value, postProcessorName)
			return

		if isinstance(value, DumpMixin):
			self._dumpObj(extraPrefix, value)
			return

		self.outputLines.append(self.prefix + extraPrefix + repr(value))
	#

	################################################################################################################################
	#### Type specific dump methods
	################################################################################################################################

	def _isDumpableObj(self, obj):
		if hasattr(obj, "_dump"):
			return True
		if hasattr(obj, "_dumpVarNames"):
			return True
		return False
	#

	#
	# Dump the specified object.
	#
	def _dumpObj(self, extraPrefix:str, value:object, postProcessorName:str = None):
		self.outputLines.append(self.prefix + extraPrefix + "<" + value.__class__.__name__ + "(")

		ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
		with ctx as ctx2:
			if hasattr(value, "_dump"):
				value._dump(ctx2)
			elif hasattr(value, "_dumpVarNames"):
				ctx2.dumpVars(value)
			else:
				raise Exception("Improper object encountered for prettyprinting!")

		self.outputLines.append(self.prefix + ")>")
	#

	#
	# Dump the specified dictionary.
	#
	def _dumpDict(self, extraPrefix:str, value:dict, postProcessorName:str = None):
		e = "dict:" if self.__s.showComplexStructsWithType else ""

		self.outputLines.append(self.prefix + extraPrefix + e + "{")

		ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
		with ctx as ctx2:
			for k, v in value.items():
				if postProcessorName == "omitValues":
					v = _OMITTED
				ctx2._dumpX(self._dictKeyToStr(k) + " : ", v)
				self.outputLines[-1] += ","

		self.outputLines.append(self.prefix + "}")
	#

	def _dumpOrderedDict(self, extraPrefix:str, value:dict, postProcessorName:str = None):
		e = "OrderedDict:" if self.__s.showComplexStructsWithType else ""

		self.outputLines.append(self.prefix + extraPrefix + e + "{")

		ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
		with ctx as ctx2:
			for k, v in value.items():
				ctx2._dumpX(self._dictKeyToStr(k) + " : ", v)
				self.outputLines[-1] += ","

		self.outputLines.append(self.prefix + "}")
	#

	#
	# Dump the specified list.
	#
	def _dumpList(self, extraPrefix:str, value:list, postProcessorName:str = None):
		e = "list:" if self.__s.showComplexStructsWithType else ""

		if self._canCompactSequence(value):
			self.outputLines.append(self.prefix + extraPrefix + e + "[ " + self._compactSequence(value) + " ]")

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "[")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				for vItem in value:
					ctx2._dumpX("", vItem)
					self.outputLines[-1] += ","

			self.outputLines.append(self.prefix + "]")
	#

	#
	# Dump the specified tuple.
	#
	def _dumpTuple(self, extraPrefix:str, value:set, postProcessorName:str = None):
		e = "tuple:" if self.__s.showComplexStructsWithType else ""

		if self._canCompactSequence(value):
			self.outputLines.append(self.prefix + extraPrefix + e + "( " + self._compactSequence(value) + " )")

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "(")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				for vItem in value:
					ctx2._dumpX("", vItem)
					self.outputLines[-1] += ","

			self.outputLines.append(self.prefix + ")")
	#

	#
	# Dump the specified set.
	#
	def _dumpSet(self, extraPrefix:str, value:set, postProcessorName:str = None):
		e = "set:" if self.__s.showComplexStructsWithType else ""

		sequence = sorted(value)

		if self._canCompactSequence(sequence):
			self.outputLines.append(self.prefix + extraPrefix + e + "{ " + self._compactSequence(sequence) + " }")

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "{")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				for vItem in sequence:
					ctx2._dumpX("", vItem)
					self.outputLines[-1] += ","

			self.outputLines.append(self.prefix + "}")
	#

	#
	# Dump the specified frozen set.
	#
	def _dumpFrozenSet(self, extraPrefix:str, value:frozenset, postProcessorName:str = None):
		e = "frozenset:" if self.__s.showComplexStructsWithType else "frozenset"

		sequence = sorted(value)

		if self._canCompactSequence(sequence):
			self.outputLines.append(self.prefix + extraPrefix + e + "{ " + self._compactSequence(sequence) + " }")

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "{")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				for vItem in sequence:
					ctx2._dumpX("", vItem)
					self.outputLines[-1] += ","

			self.outputLines.append(self.prefix + "}")
	#

	def _dumpPrimitive(self, extraPrefix:str, value, postProcessorName:str = None):
		self.outputLines.append(self.prefix + extraPrefix + self._primitiveValueToStr(value, postProcessorName))
	#

	def _dumpOmitted(self, extraPrefix:str, value, postProcessorName:str = None):
		self.outputLines.append(self.prefix + extraPrefix + "...")
	#

	################################################################################################################################
	#### Helper methods
	################################################################################################################################

	def _canCompactSequence(self, someSequence):
		if len(someSequence) > self.__s.compactSequencLimit:
			return False
		for v in someSequence:
			if (v is not None) and (type(v) not in [ int, str, float, bool ]):
				return False
		return True
	#

	def _compactSequence(self, someSequence) -> str:
		ret = []
		for v in someSequence:
			ret.append(self._primitiveValueToStr(v))
		return ", ".join(ret)
	#

	#
	# Converts a single dictionary key to str
	#
	def _dictKeyToStr(self, value):
		if value is None:
			return "(null)"
		else:
			if self.__s.showDictKeysWithType:
				if isinstance(value, float):
					return "float:" + repr(value)
				elif isinstance(value, bool):
					return "bool:" + repr(value)
				elif isinstance(value, int):
					return "int:" + repr(value)
				else:
					return type(value).__name__ + ":" + repr(value)
			else:
				return repr(value)
	#

	#
	# Converts a single primitive value to str
	#
	def _primitiveValueToStr(self, value, postProcessorName:str = None):
		if value is None:
			return "(null)"
		else:
			if self.__s.showPrimitivesWithType:
				if isinstance(value, float):
					return "float:" + repr(value)
				elif isinstance(value, bool):
					return "bool:" + repr(value)
				elif isinstance(value, int):
					return "int:" + repr(value)
				elif isinstance(value, str):
					if postProcessorName:
						if postProcessorName not in POST_PROCESSORS:
							raise Exception("No such postprocessor: " + repr(postProcessorName))
						postProcessor = POST_PROCESSORS[postProcessorName]
						return "str:" + repr(postProcessor(value))
					else:
						return "str:" + repr(value)
				else:
					return type(value).__name__ + ":" + repr(value)
			else:
				if isinstance(value, str):
					if postProcessorName:
						if postProcessorName not in POST_PROCESSORS:
							raise Exception("No such postprocessor: " + repr(postProcessorName))
						postProcessor = POST_PROCESSORS[postProcessorName]
						return repr(postProcessor(value))
					else:
						return repr(value)
				else:
					return repr(value)
	#

	################################################################################################################################
	#### Magic methods
	################################################################################################################################

	def __enter__(self):
		return self
	#

	def __exit__(self, *args):
		if self.__exitAppend:
			self.outputLines.append(self.__exitAppend)
		return False
	#

#




#
# Now let's register the types
#
if not DumpCtx._TYPE_MAP:
	DumpCtx._TYPE_MAP[set] = DumpCtx._dumpSet
	DumpCtx._TYPE_MAP[frozenset] = DumpCtx._dumpFrozenSet
	DumpCtx._TYPE_MAP[tuple] = DumpCtx._dumpTuple
	DumpCtx._TYPE_MAP[list] = DumpCtx._dumpList
	DumpCtx._TYPE_MAP[collections.OrderedDict] = DumpCtx._dumpOrderedDict
	DumpCtx._TYPE_MAP[dict] = DumpCtx._dumpDict
	DumpCtx._TYPE_MAP[int] = DumpCtx._dumpPrimitive
	DumpCtx._TYPE_MAP[float] = DumpCtx._dumpPrimitive
	DumpCtx._TYPE_MAP[bool] = DumpCtx._dumpPrimitive
	DumpCtx._TYPE_MAP[str] = DumpCtx._dumpPrimitive
	DumpCtx._TYPE_MAP[_Omitted] = DumpCtx._dumpOmitted






class Dumper(object):

	def __init__(self):
		self.__outputLines = []
		self.__contexts = []
		self.__currentPrefix = ""
	#

	def createContext(self, obj, prefix:str = None):
		if prefix is not None:
			assert isinstance(prefix, str)
		else:
			prefix = ""

		return DumpCtx(DEFAULT_DUMPER_SETTINGS, self.__outputLines, None, prefix)
	#

	def print(self, printFunc = None):
		if printFunc is None:
			printFunc = print
		else:
			assert callable(printFunc)

		for line in self.__outputLines:
			printFunc(line)
	#

#





class DumpMixin:

	def dump(self, prefix:str = None, printFunc = None):
		dumper = Dumper()
		with dumper.createContext(self, prefix) as dumper2:
			if not dumper2._isDumpableObj(self):
				raise Exception("Improper object encountered for prettyprinting!")
			dumper2._dumpObj("", self)
		dumper.print(printFunc)
	#

#












