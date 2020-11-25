import random

groups = [[1, 2, 5, 9], [0, 3, 10, 14, 19], [4, 7, 8, 11, 12, 13, 15, 17, 18], [6, 16]]
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

for i in range(0, 20):
	for j in range(i + 1, 20): 
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
	total = key + value
	vals = [s for s in total.split() if s.isdigit() or s == '.']
	
	# print([i for i in vals])

inp = open('generated/20.in', 'w')

for key, value in maindict.items():
	myStr = key + value
	myStr = myStr.replace(']', ' ')
	myStr = myStr.replace('[', ' ')
	myStr = myStr.replace(',', ' ')
	myStr = myStr.replace('\'', ' ')
	# print(myStr)
	vals = [s for s in myStr.split() if s.replace('.', '').isdigit()]
	inp.write(vals[0] + ' ' + vals[1] + ' ' + vals[2] + ' ' + vals[3] + '\n')
inp.close

out = open('generated/20.out', 'w')

assignment = []

for i in range(20):
	for j in range(len(groups)):
		if i in groups[j]:
			assignment.append(str(i) + ' ' + str(j))

for a in assignment:
	out.write(a + '\n')


# for i in range(len(groups)):
# 	for j in groups[i]:
# 		assignment.append(str(j) + ' ' + str(i))

# assignment.sort()
print(assignment)

out.close


print(len(maindict))