#!/usr/bin/python3





import jk_prettyprintobj





class Matrix(jk_prettyprintobj.DumpMixin):

	def __init__(self, m):
		self.__m = m
		self.__nRows = len(m)
		self.__nColumns = len(m[0])
	#

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar("nRows", self.__nRows)
		ctx.dumpVar("nColumns", self.__nColumns)
		ctx.dumpVar("m", self.__m, "float_round3")
	#

#








m = Matrix([
	[	1,	2,	3 	],
	[	4,	5,	6 	],
	[	7,	8,	9.1234567	],
])

m.dump()









