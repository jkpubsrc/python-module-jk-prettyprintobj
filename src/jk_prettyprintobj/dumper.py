

import typing
import collections

from .RawValue import RawValue
from .DumperSettings import DumperSettings
#from ._Hex import _Hex
#from ._Bits import _Bits
from ._ConverterFunctions import _ConverterFunctions as _CF
from ._ByteChunker import _ByteChunker








DEFAULT_DUMPER_SETTINGS = DumperSettings()






_PRIMITIVE_POST_PROCESSORS = {
	# map associating processor name to tuple consisting of type (or type list) and callable

	"shorten": (str, _CF.str_shortenText),
	"hex": (int, _CF.int_toHex),
	"bit": (int, _CF.int_toBits),
	"round1": ((float, int), _CF.float_roundTo1FractionDigits),
	"round2": ((float, int), _CF.float_roundTo2FractionDigits),
	"round3": ((float, int), _CF.float_roundTo3FractionDigits),
	"round4": ((float, int), _CF.float_roundTo4FractionDigits),
	"round5": ((float, int), _CF.float_roundTo5FractionDigits),
	"round6": ((float, int), _CF.float_roundTo6FractionDigits),
	"round7": ((float, int), _CF.float_roundTo7FractionDigits),

	"str_shorten": (str, _CF.str_shortenText),
	"float_round7": ((float, int), _CF.float_roundTo7FractionDigits),
	"float_round6": ((float, int), _CF.float_roundTo6FractionDigits),
	"float_round5": ((float, int), _CF.float_roundTo5FractionDigits),
	"float_round4": ((float, int), _CF.float_roundTo4FractionDigits),
	"float_round3": ((float, int), _CF.float_roundTo3FractionDigits),
	"float_round2": ((float, int), _CF.float_roundTo2FractionDigits),
	"float_round1": ((float, int), _CF.float_roundTo1FractionDigits),
	"int_hex": (int, _CF.int_toHex),
	"int_bit": (int, _CF.int_toBits),
}




class _Omitted:
	pass
#

_OMITTED = _Omitted()





DumpCtx = typing.NewType("DumpCtx", object)

class DumpCtx(object):

	_TYPE_MAP:typing.Dict[type,typing.Callable[[DumpCtx,str,typing.Any,typing.Union[str,None]],None]] = {}				# type -> function

	def __init__(self, s:DumperSettings, outputLines:list, exitAppend:str, prefix:str):
		self.__s = s
		self.outputLines = outputLines
		self.__exitAppend = exitAppend
		self.prefix = prefix
	#

	################################################################################################################################
	#### Methods that should be called by implementors
	################################################################################################################################

	#
	# if you implement `void _dump(DumpCtx ctx)` invoke this method to dump a specific variable explicitely.
	#
	def dumpVar(self, varName:str, value, processorName:str = None) -> None:
		self._dumpX(varName + " = ", value, processorName)
	#

	def dumpVarRaw(self, varName:str, value:RawValue) -> None:
		self._dumpX(varName + " = ", value)
	#

	#
	# This method is invoked if an object implements _dumpVarNames()
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

			processorName = None
			pos = varName.find(":")
			if pos == 0:
				raise Exception()
			elif pos > 0:
				processorName = varName[pos+1:]
				varName = varName[:pos]

			value = getattr(caller, varName)
			self._dumpX(varName + " = ", value, processorName)
	#

	################################################################################################################################
	#### Dispatcher method
	################################################################################################################################

	#
	# This method outputs a value (recursively). It is the main dump method.
	# To achieve this this method analyses the data type of the specified value and invokes individual type processing methods if available.
	#
	# @param		str extraPrefix			(required) A prefix to use
	# @param		any value				(optional) The value to print
	# @param		str? processorName		(optional) A value output processor
	#
	def _dumpX(self, extraPrefix:str, value, processorName:str = None):
		if value is None:
			self._dumpPrimitive(extraPrefix, None, processorName)
			return

		# is it a raw value?

		if isinstance(value, RawValue):
			if processorName is not None:
				raise Exception("Raw values can not have processors.")
			self._dumpRawValue(extraPrefix, value)
			return

		# is it one of our types?

		t = type(value)
		m = DumpCtx._TYPE_MAP.get(t)
		if m:
			m(self, extraPrefix, value, processorName)
			return

		# is it an object with a DumpMixin?

		if isinstance(value, DumpMixin):
			self._dumpObj(extraPrefix, value, processorName)
			return

		# is it derived from one of our types?

		for storedT, m in DumpCtx._TYPE_MAP.items():
			if isinstance(value, storedT):
				m(self, extraPrefix, value, processorName)
				return

		# fallback

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
	# @param	str processorName		(optional) The name of an output processor.
	#									Supports: "shorten"
	#
	def _dumpObj(self, extraPrefix:str, value:object, processorName:str = None):
		if processorName == "shorten":
			if hasattr(value, "_dumpShort"):
				value._dumpShort(ctx2)
			else:
				self.outputLines.append(self.prefix + extraPrefix + "<" + value.__class__.__name__ + "(...)>")

		else:
			self.outputLines.append(self.prefix + extraPrefix + "<" + value.__class__.__name__ + "(")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				if hasattr(value, "_dump"):
					value._dump(ctx2)
				elif hasattr(value, "_dumpVarNames"):
					ctx2.dumpVars(value)
				else:
					raise Exception("Improper object encountered for prettyprinting: " + type(value).__name__)

			self.outputLines.append(self.prefix + ")>")
	#

	#
	# Dump the specified dictionary.
	#
	# @param		str processorName			(optional) The processor name. This name is passed to recursive calls of _dumpX() so that it is applied
	#											to every value. Additionally if "shorten" is specified the dictionary itself will be shortened.
	#
	def _dumpDict(self, extraPrefix:str, value:dict, processorName:str = None):
		e = (type(value).__name__ + ":") if self.__s.showComplexStructsWithType else ""

		self.outputLines.append(self.prefix + extraPrefix + e + "{")

		ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
		with ctx as ctx2:
			i = 0
			for k, v in value.items():
				if processorName == "shorten":
					if i >= 3:
						ctx2._dumpRawValue("", RawValue("..."))
						break
				if processorName == "omitValues":
					v = _OMITTED
				ctx2._dumpX(self._dictKeyToStr(k) + " : ", v)
				self.outputLines[-1] += ","
				i += 1

		self.outputLines.append(self.prefix + "}")
	#

	def _dumpOrderedDict(self, extraPrefix:str, value:dict, processorName:str = None):
		e = (type(value).__name__ + ":") if self.__s.showComplexStructsWithType else ""

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
	# @param		str processorName			(optional) The processor name. This name is passed to recursive calls of _dumpX() so that it is applied
	#											to every value. Additionally if "shorten" is specified the list itself will be shortened.
	#
	def _dumpList(self, extraPrefix:str, value:list, processorName:str = None):
		e = (type(value).__name__ + ":") if self.__s.showComplexStructsWithType else ""

		if self._canCompactSequence(value):
			rawText = self._compactSequence(value, processorName)
			self.outputLines.append(self.prefix + extraPrefix + e + "[ " + rawText + " ]")

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "[")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				i = 0
				for vItem in value:
					if processorName == "shorten":
						if i >= 3:
							ctx2._dumpRawValue("", RawValue("..."))
							break
					ctx2._dumpX("", vItem, processorName)
					self.outputLines[-1] += ","
					i += 1

			self.outputLines.append(self.prefix + "]")
	#

	#
	# Dump the specified byte array.
	#
	def _dumpBytes(self, extraPrefix:str, value:bytes, processorName:str = None):
		e = (type(value).__name__ + ":") if self.__s.showComplexStructsWithType else ""

		if len(value) <= self.__s.bytesLineSize:
			self.outputLines.append(self.prefix + extraPrefix + e + repr(value))

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "<")

			for sOfs, chunk, sAscii in _ByteChunker.chunkWithOfs(self.__s, value, processorName):
				self.outputLines.append(self.prefix + "\t" + sOfs + "  " + chunk + "  " + sAscii)

			if len(value) == 1:
				self.outputLines.append(self.prefix + "\ttotal: 1 byte")
			else:
				self.outputLines.append(self.prefix + "\ttotal: " + str(len(value)) + " bytes")

			self.outputLines.append(self.prefix + ">")
	#

	#
	# Dump the specified tuple.
	#
	# @param		str processorName			(optional) The processor name. This name is passed to recursive calls of _dumpX() so that it is applied
	#											to every value. Additionally if "shorten" is specified the list itself will be shortened.
	#
	def _dumpTuple(self, extraPrefix:str, value:set, processorName:str = None):
		e = (type(value).__name__ + ":") if self.__s.showComplexStructsWithType else ""

		if self._canCompactSequence(value):
			rawText = self._compactSequence(value, processorName)
			self.outputLines.append(self.prefix + extraPrefix + e + "( " + rawText + " )")

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "(")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				i = 0
				for vItem in value:
					if processorName == "shorten":
						if i >= 3:
							ctx2._dumpRawValue("", RawValue("..."))
							break
					ctx2._dumpX("", vItem, processorName)
					self.outputLines[-1] += ","
					i += 1

			self.outputLines.append(self.prefix + ")")
	#

	#
	# Dump the specified set.
	#
	def _dumpSet(self, extraPrefix:str, value:set, processorName:str = None):
		e = (type(value).__name__ + ":") if self.__s.showComplexStructsWithType else ""

		sequence = sorted(value)

		if self._canCompactSequence(sequence):
			self.outputLines.append(self.prefix + extraPrefix + e + "{ " + self._compactSequence(sequence, processorName) + " }")

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "{")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				for vItem in sequence:
					ctx2._dumpX("", vItem, processorName)
					self.outputLines[-1] += ","

			self.outputLines.append(self.prefix + "}")
	#

	#
	# Dump the specified frozen set.
	#
	def _dumpFrozenSet(self, extraPrefix:str, value:frozenset, processorName:str = None):
		e = (type(value).__name__ + ":") if self.__s.showComplexStructsWithType else ""

		sequence = sorted(value)

		if self._canCompactSequence(sequence):
			self.outputLines.append(self.prefix + extraPrefix + e + "{ " + self._compactSequence(sequence, processorName) + " }")

		else:
			self.outputLines.append(self.prefix + extraPrefix + e + "{")

			ctx = DumpCtx(self.__s, self.outputLines, None, self.prefix + "\t")
			with ctx as ctx2:
				for vItem in sequence:
					ctx2._dumpX("", vItem, processorName)
					self.outputLines[-1] += ","

			self.outputLines.append(self.prefix + "}")
	#

	def _dumpPrimitive(self, extraPrefix:str, value, processorName:str = None):
		self.outputLines.append(self.prefix + extraPrefix + self._primitiveValueToStr(value, processorName))
	#

	def _dumpRawValue(self, extraPrefix:str, value:RawValue):
		if isinstance(value.textOrLines, str):
			self.outputLines.append(self.prefix + extraPrefix + value.textOrLines)
			return

		firstLine = value.textOrLines[0]
		moreLines = value.textOrLines[1:]

		self.outputLines.append(self.prefix + extraPrefix + firstLine)

		_prefix2 = self.prefix + " " * len(extraPrefix)
		for line in moreLines:
			self.outputLines.append(_prefix2 + line)
	#

	def _dumpOmitted(self, extraPrefix:str, value, processorName:str = None):
		self.outputLines.append(self.prefix + extraPrefix + "...")
	#

	################################################################################################################################
	#### Helper methods
	################################################################################################################################

	def _canCompactSequence(self, someSequence):
		if len(someSequence) > self.__s.compactSequenceLengthLimit:
			return False
		for v in someSequence:
			if v is not None:
				if type(v) not in [ int, str, float, bool ]:
					return False
				if isinstance(v, str):
					if len(v) > self.__s.compactSequenceItemLengthLimit:
						return False
		return True
	#

	# TODO: support "shorten" to shorten the list
	def _compactSequence(self, someSequence, processorName:str = None) -> str:
		ret = []
		for v in someSequence:
			ret.append(self._primitiveValueToStr(v, processorName))
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
	def _primitiveValueToStr(self, value, processorName:str = None):
		if value is None:
			return "(null)"
		else:
			# process value before converting it to str
			if processorName:
				if processorName not in _PRIMITIVE_POST_PROCESSORS:
					raise Exception("No such postprocessor: " + repr(processorName))
				postProcessorTypeCompatibility, postProcessor = _PRIMITIVE_POST_PROCESSORS[processorName]
				if isinstance(value, postProcessorTypeCompatibility):
					value = postProcessor(value)

			# return value as str
			if self.__s.showPrimitivesWithType:
				if isinstance(value, float):
					return "float:" + repr(value)
				elif isinstance(value, bool):
					return "bool:" + repr(value)
				elif isinstance(value, int):
					return "int:" + repr(value)
				elif isinstance(value, str):
					return "str:" + repr(value)
				else:
					return type(value).__name__ + ":" + repr(value)
			else:
				if isinstance(value, str):
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
	DumpCtx._TYPE_MAP[bytes] = DumpCtx._dumpBytes
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

	def toStr(self) -> str:
		return "\n".join(self.__outputLines)
	#

#





################################################################################################################################
################################################################################################################################
"""

Dumpable objects should be defined like this:

	class FooBar(SomeBaseClassA,SomeMixinB,jk_prettyprintobj.DumpMixin)
		....
	#

Dumpable objects should then implement one of these two methods:

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar(...)
	#

or:

	def _dumpVarNames(self) -> typing.List[str]:
		return [
			"....",
		]
	#

and maybe additionally:

	def _dumpShort(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar(...)
	#

"""
################################################################################################################################
################################################################################################################################




class DumpMixin:

	__slots__ = tuple()

	def __dump(self, prefix:str = None) -> Dumper:
		dumper = Dumper()
		with dumper.createContext(self, prefix) as dumper2:
			if not dumper2._isDumpableObj(self):
				raise Exception("Improper object encountered for prettyprinting: " + self.__class__.__name__ + " - Either implement _dump(ctx:DumpCtx) or _dumpVarNames()!")
			dumper2._dumpObj("", self)
		return dumper
	#

	def dump(self, prefix:str = None, printFunc = None) -> None:
		dumper = self.__dump(prefix)
		dumper.print(printFunc)
	#

	def dumpToStr(self, prefix:str = None) -> str:
		dumper = self.__dump(prefix)
		return dumper.toStr()
	#

	def dumpToFile(self, filePath:str) -> None:
		dumper = self.__dump()
		assert isinstance(filePath, str)
		with open(filePath, "w", newline="\n", encoding="UTF-8") as fout:
			fout.write(dumper.toStr())
	#

#












