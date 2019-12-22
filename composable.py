#This code was written by Chris Llaga as a Spreadsheet Evaluation Tool

import re
import sys

#Reads the input file into a list
def readInput(inputFile) :
    with open(inputFile) as file :
        content = file.readlines()
    return content

#Takes the input list and turns it into a 2d list
def inputToArray(content) :
    array = []
    for row in content :
        curr = []
        row = row.lower().strip().split(',')
        for col in row :
            curr += [col]
        array += [curr]
    return array

#Takes a string and translates it into corresponding
#2d array position with starting index at 0
#ex 'a1', 'z2', 'aa3', 'za4'
#   [0][0], [25][1], [26][2], [677][3]
def translateLocation(location, array) :
    #Separates the string into the alphabetic and numeric portion
    match = re.match(r"([a-z]+)([0-9]+)", location, re.I)
    if match :
        items = match.groups()
    else :
        sys.exit('Error, string does not translate to a grid location: ' + str(location))
    letters = items[0]
    #Calculates xcoord position by using a base 26 number system with letters assigned as symbols
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
    return([letterToNumber, number])

#Simple getter function when passed coordinates within the 2d array
def retrieveContents(location, array) :
    try :
        print('// Retrieving contents from ' + str(location) + ' to: ' + str(array[location[0]][location[1]]))
        return array[location[0]][location[1]]
    except :
        sys.exit('Error, cell does not exist: ' + str(location))

#Evaluates the cell using a stack system
def evaluateCell(cell, array, history) :
    stack = []
    cell = cell.strip().split(' ')
    print('-- Evaluating cell: ' + str(cell))
    for operand in cell :
        if(operand != ' ') :
            #Check if the operand can be turned into a float
            #Otherwise, pass. This is to turn signed numbers into floats
            try :
                operand = float(operand)
            except :
                pass
            #If the operand is just a number, nothing extra needs to be done
            if(type(operand) == float or operand.isnumeric()) :
                stack.append(float(operand))
                print('++ Adding to the stack as a number: ' + str(operand))
            #If the operand is an alnum, then it is a cell reference, so go
            #to that cell and evaluate. This is an area where efficiency can be improved:
            #If I can find a way to modify the list while traversing it, then cells do not
            #have to be recalculated whenever they are referenced.
            elif(operand.isalnum()) :
                location = translateLocation(operand, array)
                #The history stack keeps track of which cells have been visited
                history.append(location)
                print('$$ Adding to history: ' + str(location))
                print('$$ Current history: ' + str(history))
                #If the cell has been visited more than once, then it is referencing itself
                if(history.count(location) > 1) :
                    sys.exit('Error, self-referential cells: ' + str(cell))
                contents = retrieveContents(location, array)
                value = evaluateCell(contents, array, history)
                stack.append(float(value))
                #Since this cell reference has been resolved, remove it from history
                history.pop()
                print('++ Adding to the stack the retrieved value')
            else :
                #Anything not alphanumeric is a symbol, so do maths according to the symbol
                try :
                    firstNum = float(stack.pop())
                    secondNum = float(stack.pop())
                except :
                    sys.exit('Error, not enough operands in cell before operation (or invalid operand): ' + str(cell))
                if(operand == '+') :
                    stack.append(firstNum + secondNum)
                if(operand == '-') :
                    stack.append(firstNum - secondNum)
                if(operand == '*') :
                    stack.append(firstNum * secondNum)
                if(operand == '/') :
                    stack.append(firstNum / secondNum)
                print('++ Doing math: ' + str(operand))
            print('== Current stack: ' + str(stack))
    #Check if the stack has properly resolved
    if(len(stack) == 1) :
        if(stack[0].is_integer()) :
            return int(stack[0])
        return stack[0]
    else :
        sys.exit('Error, stack has not properly resolved: ' + str(stack))

#Populates the final grid by iterating through
#the original 2d array and applying the evaluateCell function
def evaluateGrid(array) :
    grid = []
    for row in array :
        curr = []
        for col in row :
            print('^^^ START')
            value = evaluateCell(col, array, [])
            curr.append(value)
            print('^^^ END')
        grid.append(curr)
    return grid

#Writes the grid to the output file, spaced evenly
def writeOutput(array, outputFile) :
    with open(outputFile, 'w') as f:
        for row in array:
            for cell in row :
                f.write("%s " % cell)
            f.write("\n")

#Uses the functions to output the grid to a file
def main(inputFile, outputFile) :
    content = readInput(inputFile)
    array = inputToArray(content)
    grid = evaluateGrid(array)
    writeOutput(grid, outputFile)
    print('Done.')

#Takes the command line arguments for input and output file locations
#If ran from outside the command line, will ask for input
if __name__== "__main__":
    if(len(sys.argv) < 2) :
        print('Spreadsheet Evaluator by Chris Llaga')
        inputFile = input('Please enter the input file name: ')
        outputFile = input('Please enter the output file name: ')
        main(inputFile, outputFile)
        input('Press the enter key to exit.')
    else :
        main(sys.argv[1], sys.argv[2])