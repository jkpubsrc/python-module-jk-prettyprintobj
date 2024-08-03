

import codecs
import math
import typing

from .DumperSettings import DumperSettings





class _ByteChunker(object):

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

	@staticmethod
	def _x_byteChunkToHex(data:bytes) -> str:
		hexSpanLength = 16		# == 8 bytes for a span

		s = codecs.encode(data, "hex").decode("ascii")
		chunks = [ s[i:i+hexSpanLength] for i in range(0, len(s), hexSpanLength) ]
		return " ".join(chunks)
	#

	@staticmethod
	def _x_byteChunkToASCII(data:bytes) -> str:
		spanLength = 8		# == 8 bytes for a span

		ret = []
		for i, b in enumerate(data):
			if (i % spanLength) == 0:
				ret.append(" ")
			if 32 <= b <= 127:
				ret.append(chr(b))
			else:
				ret.append(".")

		return "".join(ret)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	#
	# Creates data for output.
	#
	# @param		DumperSettings settings		The settings object that contains <c>settings.compactBytesLinesLengthLimit</c>
	# @param		bytes data					The full data block to process
	# @param		str? processorName			Understands "shorten" to provide shortened output,
	#											respecting <c>settings.compactBytesLinesLengthLimit</c> in that cae
	# @return		tuple<str,str,str>[]		Returns a generator that provides tuples of the following values:
	#											* str offset part
	#											* str hex data part
	#											* str ascii data part
	#
	@staticmethod
	def chunkWithOfs(settings:DumperSettings, data:bytes, processorName:str = None) -> typing.Generator[typing.Tuple[str,str,str],typing.Tuple[str,str,str],typing.Tuple[str,str,str]]:
		assert isinstance(settings, DumperSettings)
		assert isinstance(data, bytes)
		chunkSize = settings.bytesLineSize
		assert isinstance(chunkSize, int)
		assert chunkSize > 0
		hexStrPadded = chunkSize*2 + math.ceil(chunkSize / 8) - 1
		if processorName is not None:
			assert isinstance(processorName, str)

		# ----

		nTotalLength = len(data)
		nTotalLines = math.ceil(nTotalLength / chunkSize)
		formatStrFragment = None
		formatStrFragmentEllipsis = None
		if nTotalLength <= 256*256:
			formatStrFragment = "{:04x}"
			formatStrFragmentEllipsis = "... "
		elif nTotalLength <= 256*256*256:
			formatStrFragment = "{:06x}"
			formatStrFragmentEllipsis = "...   "
		else:
			formatStrFragment = "{:08x}"
			formatStrFragmentEllipsis = "...     "

		# ----

		skipFrom = -1
		skipTo = -1
		if processorName:
			if processorName == "shorten":
				skipFrom = settings.compactBytesLinesLengthLimit
				skipTo = nTotalLines - 4
				if skipFrom >= skipTo:
					skipFrom = -1
					skipTo = -1
			else:
				raise Exception("No such postprocessor: " + repr(processorName))

		# ----

		if skipFrom < 0:
			# direct loop, no addtional if statements
			iFrom = 0
			iTo = chunkSize
			while iFrom < len(data):
				chunk = data[iFrom:iTo]
				yield formatStrFragment.format(iFrom), _ByteChunker._x_byteChunkToHex(chunk).ljust(hexStrPadded), _ByteChunker._x_byteChunkToASCII(chunk)
				iFrom = iTo
				iTo += chunkSize
		else:
			# loop with if statements
			lineNo = 0
			iFrom = 0
			iTo = chunkSize
			while iFrom < len(data):
				chunk = data[iFrom:iTo]
				if skipFrom <= lineNo <= skipTo:
					if skipFrom == lineNo:
						yield formatStrFragmentEllipsis, "...".ljust(hexStrPadded), "..."
				else:
					yield formatStrFragment.format(iFrom), _ByteChunker._x_byteChunkToHex(chunk).ljust(hexStrPadded), _ByteChunker._x_byteChunkToASCII(chunk)
				iFrom = iTo
				iTo += chunkSize
				lineNo += 1
	#

#







