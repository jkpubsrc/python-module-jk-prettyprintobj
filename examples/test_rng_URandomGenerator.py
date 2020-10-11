#!/usr/bin/env python3


import jk_utils.rng


rng = jk_utils.rng.URandomGenerator()

print()

for i in range(0, 20):
	print("nextBytes() = %s" % (rng.nextBytes(7),))
print()

for i in range(0, 20):
	print("nextUInt8() = %d" % (rng.nextUInt8(),))
print()

for i in range(0, 20):
	print("nextUInt16() = %d" % (rng.nextUInt16(),))
print()

for i in range(0, 20):
	print("nextUInt32() = %d" % (rng.nextUInt32(),))
print()

for i in range(0, 20):
	print("nextUInt64() = %d" % (rng.nextUInt64(),))
print()

for i in range(0, 20):
	print("nextInt8() = %d" % (rng.nextInt8(),))
print()

for i in range(0, 20):
	print("nextInt16() = %d" % (rng.nextInt16(),))
print()

for i in range(0, 20):
	print("nextInt32() = %d" % (rng.nextInt32(),))
print()

for i in range(0, 20):
	print("nextInt64() = %d" % (rng.nextInt64(),))
print()

for i in range(0, 20):
	print("nextString() = %s" % (rng.nextString("abcde", 20),))
print()

for i in range(0, 20):
	print("nextCharacter() = %s" % (rng.nextCharacter("abcde"),))
print()

for i in range(0, 20):
	print("nextUInt32Bounded() = %d" % (rng.nextUInt32Bounded(6),))
print()

for i in range(0, 20):
	print("nextFloat() = %f" % (rng.nextFloat(),))
print()







