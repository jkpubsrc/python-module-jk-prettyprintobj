#!/usr/bin/env python3




import jk_utils





"""
table = core.TextCanvas()
table.drawRectangle(0, 0, 5, 3, bDoubleBorderBottom = True)
table.drawRectangle(5, 0, 15, 3, bDoubleBorderBottom = True)
table.drawRectangle(0, 3, 5, 7, bDoubleBorderTop = True)
table.drawRectangle(0, 7, 5, 9)
table.drawRectangle(5, 7, 15, 9)
table.print()
"""



table = jk_utils.TextTable()
table.setCell(0, 0, "abcdef", 1, 1)
table.setCell(1, 0, "ghi", 1, 1)
table.setCell(0, 1, [ "jkl", "mnop" ], 1, 1)
table.setCell(1, 1, "qrstuvwxyz", 1, 1)
table.setCell(0, 2, "aeiouaeiouaeiou", 2, 1)
table.setHeadingRow(0)
table.dump()
table.print()




