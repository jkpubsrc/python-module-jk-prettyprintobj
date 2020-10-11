#!/usr/bin/env python3




import jk_utils






class EnumState(jk_utils.EnumBase):

	A = 0, "A"
	B = 1, "B"
	C = 2, "C"

#



def sayHelloB():
	print("Hello, B!")
#

def sayFromAToB():
	print("Going from A to B.")
#

def leavingA():
	print("Leave A")
#

def sayAlways():
	print("Always")
#




stateManager = jk_utils.StateManager(EnumState.allStates(), EnumState.A)


stateManager.registerActionFrom(EnumState.A, leavingA, 0, "leavingA")
stateManager.registerActionTo(EnumState.B, sayFromAToB, 0, "sayFromAToB")
stateManager.registerActionFromTo(EnumState.A, EnumState.B, sayHelloB, 0, "sayHelloB")
stateManager.registerAction(sayAlways, 0, "sayAlways")



stateManager.dump()


print()
print("switching to: A")
print()

stateManager.switchState(EnumState.A)

print()
print("switching to: B")
print()

stateManager.switchState(EnumState.B)

print()
print("switching to: C")
print()

stateManager.switchState(EnumState.C)











