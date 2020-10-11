#!/usr/bin/env python3



import jk_console

from jk_utils import TimeLimitedCache



cache = TimeLimitedCache(5)




cache.put("a", "Something")




print()
print("Enter 'x' to see if the data is still there.")
print()




while True:
	keyChar = input()
	if keyChar == "x":
		item = cache.get("a", False)
		print(item)

