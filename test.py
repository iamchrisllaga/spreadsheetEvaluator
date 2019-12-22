import re

def foo(location) :
	match = re.match(r"([a-z]+)([0-9]+)", location, re.I)
	if match :
		items = match.groups()
	letters = items[0]
	letterToNumber = 0
	count = 0
	for char in reversed(letters) :
		charValue = ord(char) - 96
		letterToNumber += charValue * (27 ** count)
		letterToNumber -= charValue * count
		count += 1
	letterToNumber -= 1
	number = int(items[1]) - 1
	print('// Translating locations from ' + str(location) + ' to : [' + str(letterToNumber) + ', ' + str(number) + ']')
	print([letterToNumber, number])

foo('za1')