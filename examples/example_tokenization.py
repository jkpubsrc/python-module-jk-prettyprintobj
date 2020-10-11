#!/usr/bin/env python3



import re

import jk_utils
from jk_utils.tokenizer2 import *



# The following pseudoconstant receives the text data we want to parse.


TEXT = """
[General Settings]
tcpPort=12345
dataDirPath=/srv/MyProgram/data
logDirPath=/home/MyHome/My Files/log
"""


# As you can see we use some kind of INI-File format here. We deliberately choose this example as tokenizing it is
# more complex than you might think on first glance: We need to distinguish between section lines and key-value-lines.
# Both need to be parsed differently: Section lines end with a "]" which is not part of the section name token while
# a value token within a key-value-pair might have a "]" as part of a token.
# That means we need to switch the way we tokenize here: As soon as we learn that we now process a section definition,
# we need to now apply the tokenization rules for section definitions. If we learn it is a regular key value pair we
# need to apply tokenization rules for key-value-pairs.


# Let's tokenize the text above. For this we are required to define a tokenizer with regular expressions.
# This tokenizer uses regular expressions that are tried one after the other in order to identify matches.
# For that a list of tuples need to be specified which can be of the following type:
# * 4 items
# 	* (required) the token type to use on match
#	* (required) the pattern to match
#	* (optional) the next state to switch to
#	* (optional) a parsing delegate to create a value from the token text
# * 6 items
#	* (required) the token type to use on match
#	* (optional) if not None a pattern to match but that will not be part of the token content
#	* (required) the pattern to match (which will be the content of the token)
#	* (optional) if not None a pattern to match but that will not be part of the token content
#	* (optional) the next state to switch to
#	* (optional) a parsing delegate to create a value from the token text
# By default whitespaces and newlines are recognized using "SPACE" and "NEWLINE" as token type names.




#
# This tokenizer tokenizes an INI-file.
#
class IniFileTokenizer(RegExBasedTableTokenizer):

	def __init__(self):
		super().__init__("std", [
			RegExBasedTokenizingTable("std", [
				( "lparen",		"\\[",					"section",	None ),
				( "word",		"[A-Za-z][a-zA-Z0-9]*", "kvp",		None ),
			]),
			RegExBasedTokenizingTable("section", [
				( "rparen",		"\\]",					None,		None ),
				( "section",	r"[^]\n]+",				None,		None ),
			]).addStateTransition("NEWLINE", "std"),
			RegExBasedTokenizingTable("kvp", [
				( "eq",			"=",					None,		None ),
				( "word",		"[A-Za-z][a-zA-Z0-9]*",	None,		None ),
				( "int",		r"[+-]?[1-9][0-9]*|0",	None,		self.__parseInt ),
				( "other",		r"[^\n]+",				None,		None ),
			]).addStateTransition("NEWLINE", "std"),
		])
	#

	def __parseInt(self, rawTokenText):
		return int(rawTokenText)
	#

#



# Now let's test the tokenizer and produce tokens. Store them in a list.

tokenizer = IniFileTokenizer()
tokens = list(tokenizer.tokenize(TEXT))
for token in tokens:
	print(token)
print()



# In order to parse the text specified above we define simple pattern schemas.

VALUE_PATTERN = TokenPatternAlternatives([
	TokenPattern("int", assignToVarTyped="v").setTag("t", "int"),
	TokenPattern("word", assignToVarTyped="v").setTag("t", "str"),
	TokenPattern("other", assignToVarTyped="v").setTag("t", "str"),
])

KVP_PATTERN = TokenPatternSequence([
	TokenPattern("word", assignToVar="k"),
	TokenPattern("eq"),
	VALUE_PATTERN,
])

SECTION_PATTERN = TokenPatternSequence([
	TokenPattern("lparen"),
	TokenPattern("section", assignToVar="s"),
	TokenPattern("rparen"),
])

NL_PATTERN = TokenPattern("NEWLINE")


# bow let's parse!

def parse(tokens:list):
	pos = 0
	while pos < len(tokens):
		bParsingSuccess, nTokensEaten, data = NL_PATTERN.tryMatch(tokens, pos)
		if bParsingSuccess:
			pos += nTokensEaten
			continue
		bParsingSuccess, nTokensEaten, data = SECTION_PATTERN.tryMatch(tokens, pos)
		if bParsingSuccess:
			yield data
			pos += nTokensEaten
			continue
		bParsingSuccess, nTokensEaten, data = KVP_PATTERN.tryMatch(tokens, pos)
		if bParsingSuccess:
			yield data
			pos += nTokensEaten
			continue
		raise Exception("Syntax error!")
#


for x in parse(tokens):
	print(">", x)



