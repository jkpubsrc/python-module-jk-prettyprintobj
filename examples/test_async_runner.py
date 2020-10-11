#!/usr/bin/env python3



import jk_console

from jk_utils import AsyncRunner



asyncRunner = AsyncRunner(debugLogPrintFunction = print)
asyncRunner.start()



def doSomething(data):
	print()
	print("#### --------------------------------")
	print("#### Doing something: " + str(data))
	print("#### --------------------------------")
	print()
#



asyncRunner.rescheduleCallable(doSomething, "abc", 5, doSomething, autoRescheduleDelay=5)




print()
print("Enter 's' to schedule or enter 'r' to reschedule some activity. Any other intput will terminate the program.")
print()




n = 1

while True:
	keyChar = input()
	if keyChar == "s":
		asyncRunner.removeScheduledCallable(doSomething)
		print("Scheduling: " + str(n))
		asyncRunner.scheduleCallable(doSomething, "Activity " + str(n), 2)
		n += 1
	elif keyChar == "r":
		print("(Re)scheduling: " + str(n))
		asyncRunner.rescheduleCallable(doSomething, "Activity " + str(n), 2, doSomething)
		n += 1
	else:
		break

