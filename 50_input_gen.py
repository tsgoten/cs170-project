import random

groups = [[1, 6, 2, 4, 15], [3, 20, 21], [0, 5, 7, 24], [8, 12], [9, 19], [10, 17, 16], [18, 11, 13, 14, 23], [25, 29, 31, 39, 42, 43, 44, 45, 49], [26, 32, 38, 46, 47, 48], [27, 28, 30, 34, 40, 41], [22, 33, 36, 35, 37]]
groupdict = {}

size = 0
for group in groups:
	size = size + len(group)

if size != 50:
	print("WRONG SIZE")
else: 
	print("CORRECT SIZE")



for group in groups: 
	for i in range(len(group)):
		for j in range(i + 1, len(group)): 
			stress = "{:.2f}".format((1 + random.uniform(-1, 1)))
			happiness = "{:.2f}".format(20 + random.uniform(-10, 10))
			#print(str(group[i]) + " " + str(group[j]) + " " + stress + " " + happiness)
			groupdict[str([group[i], group[j]])] = str([stress, happiness])

"""
for key, value in groupdict.items():
	print(key, ' : ', value)
"""

maindict = {}

for i in range(0, 50):
	for j in range(i + 1, 50): 
		if str([i, j]) not in groupdict.keys():
			stress = "{:.2f}".format((20 + random.uniform(-4, 4)))
			happiness = "{:.2f}".format(5 + random.uniform(-2, 2))
			maindict[str([i, j])] = str([stress, happiness])
		else: 
			maindict[str([i, j])] = groupdict[str([i, j])]

"""
"[41, 44]"  :  "['16.18', '3.98']"

41 44 16.18 3.98

"""

for key, value in maindict.items():
	total = key + value
	vals = [s for s in total.split() if s.isdigit() or s == '.']
	print([i for i in vals])

print(len(maindict))

