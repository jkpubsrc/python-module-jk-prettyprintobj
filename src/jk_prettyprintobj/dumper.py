

#import collections
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

	def dumpVar(self, varName:str, value):
		self._dumpX(varName + " = ", value)
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
			value = getattr(caller, varName)
			self._dumpX(varName + " = ", value)
	#

	################################################################################################################################
	#### Dispatcher method
	################################################################################################################################

	#
	# This method outputs a value (recursively).
	# To achieve this this method analyses the data type of the specified value and invokes individual type processing methods if available.
	#
	def _dumpX(self, extraPrefix:str, value):
		if value is None:
			self._dumpPrimitive(extraPrefix, value)
			return

		t = type(value)
		m = DumpCtx._TYPE_MAP.get(t)
		if m:
			m(self, extraPrefix, value)
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
	def _dumpObj(self, extraPrefix:str, value:object):
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
	def _dumpDict(self, extraPrefix:str, value:dict):
		e = "dict:" if self.__s.showComplexStructsWithType else ""

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
	def _dumpList(self, extraPrefix:str, value:list):
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
	def _dumpTuple(self, extraPrefix:str, value:tuple):
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
	def _dumpSet(self, extraPrefix:str, value:set):
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
	def _dumpFrozenSet(self, extraPrefix:str, value:frozenset):
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

	def _dumpPrimitive(self, extraPrefix:str, value):
		self.outputLines.append(self.prefix + extraPrefix + self._primitiveValueToStr(value))
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
	def _primitiveValueToStr(self, value):
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
				else:
					return type(value).__name__ + ":" + repr(value)
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
	DumpCtx._TYPE_MAP[dict] = DumpCtx._dumpDict
	DumpCtx._TYPE_MAP[int] = DumpCtx._dumpPrimitive
	DumpCtx._TYPE_MAP[float] = DumpCtx._dumpPrimitive
	DumpCtx._TYPE_MAP[bool] = DumpCtx._dumpPrimitive
	DumpCtx._TYPE_MAP[str] = DumpCtx._dumpPrimitive






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












