import random

groups = [[1, 3, 7], [0, 2, 9], [4, 5, 6, 8]]
groupdict = {}

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

for i in range(0, 10):
	for j in range(i + 1, 10): 
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
# String Output 

for key, value in maindict.items():
	myStr = key + value
	myStr = myStr.replace(']', ' ')
	myStr = myStr.replace('[', ' ')
	myStr = myStr.replace(',', ' ')
	myStr = myStr.replace('\'', ' ')
	# print(myStr)
	vals = [s for s in myStr.split() if s.replace('.', '').isdigit()]
	print(vals[0] + ' ' + vals[1] + ' ' + vals[2] + ' ' + vals[3])


print(len(maindict))


