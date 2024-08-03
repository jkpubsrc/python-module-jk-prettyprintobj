

import typing

from ._Hex import _Hex
from ._Bits import _Bits





class _ConverterFunctions(object):

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
	def str_shortenText(text:str) -> str:
		if len(text) > 40:
			return text[:40] + "..."
		else:
			return text
	#

	@staticmethod
	def float_roundTo7FractionDigits(data:typing.Union[int,float]) -> float:
		return round(data, 7)
	#

	@staticmethod
	def float_roundTo6FractionDigits(data:typing.Union[int,float]) -> float:
		return round(data, 6)
	#

	@staticmethod
	def float_roundTo5FractionDigits(data:typing.Union[int,float]) -> float:
		return round(data, 5)
	#

	@staticmethod
	def float_roundTo4FractionDigits(data:typing.Union[int,float]) -> float:
		return round(data, 4)
	#

	@staticmethod
	def float_roundTo3FractionDigits(data:typing.Union[int,float]) -> float:
		return round(data, 3)
	#

	@staticmethod
	def float_roundTo2FractionDigits(data:typing.Union[int,float]) -> float:
		return round(data, 2)
	#

	@staticmethod
	def float_roundTo1FractionDigits(data:typing.Union[int,float]) -> float:
		return round(data, 1)
	#

	@staticmethod
	def int_toHex(data:int) -> typing.Union[int,str]:
		if data < 0:
			return data
		return _Hex(data)
	#

	@staticmethod
	def int_toBits(data:int) -> typing.Union[int,str]:
		if data < 0:
			return data
		return _Bits(data)
	#

	@staticmethod
	def byteChunker(data:bytes, chunkSize:int) -> typing.Generator[bytes,bytes,bytes]:
		assert isinstance(data, bytes)
		assert isinstance(chunkSize, int)
		assert chunkSize > 0

		iFrom = 0
		iTo = chunkSize
		while iFrom < len(data):
			yield data[iFrom:iTo]
			iFrom = iTo
			iTo += chunkSize
	#

#







