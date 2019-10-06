from __future__ import print_function # will help with debugging

import copy # will allow us to deep copy our sudoku objects

import sys

class sudokuPuzzle():

	def __init__(self, file = None, puzzleCopy = None, label = None):

		self.board = {}
		
		self.puzzleDomains = {} # holds possible values for each cell in sudoku grid

		self.triedVals = set()

		self.label = 0

		self.blockMap = { # blocks are numbered sequentially starting with top left and ending with bottom right

			'1':['A1','A2','A3','B1','B2','B3','C1','C2','C3'], # block 1
			'2':['A4','A5','A6','B4','B5','B6','C4','C5','C6'], # block 2
			'3':['A7','A8','A9','B7','B8','B9','C7','C8','C9'], # block 3
			'4':['D1','D2','D3','E1','E2','E3','F1','F2','F3'], # block 4
			'5':['D4','D5','D6','E4','E5','E6','F4','F5','F6'], # block 5
			'6':['D7','D8','D9','E7','E8','E9','F7','F8','F9'], # block 6
			'7':['G1','G2','G3','H1','H2','H3','I1','I2','I3'], # block 7
			'8':['G4','G5','G6','H4','H5','H6','I4','I5','I6'], # block 8
			'9':['G7','G8','G9','H7','H8','H9','I7','I8','I9'], # block 9
		}


		if file != None: # fill board from file if one is is passed in
			self.fillBoard(file)


		elif puzzleCopy != None: # this will construct copy of sudoku puzzle from copyFrom
			self.board = copy.deepcopy(puzzleCopy.board) 
			self.puzzleDomains = copy.deepcopy(puzzleCopy.puzzleDomains)
			self.label = puzzleCopy.label
			self.triedVals = puzzleCopy.triedVals

		if label != None:
			self.label = label


	def fillBoard(self, file):

		rows = 'ABCDEFGHI'
		columns = '123456789'

		#loop through file and fill board, 0 = empty space in board
		for row in rows:
			for column in columns:

				val = file.read(1)
				while(val not in '0123456789'): #this will make sure values we store are only base 10 digits
					val = file.read(1) 

				self.board[row+column] = val


	def printBoard(self, myFile = None): # unfinished

		rows = 'ABCDEFGHI'
		columns = '123456789'

		if file == None:
			#loop through board and print 
			print("BOARD STATE: " + str(self.label))
			for row in rows:
				for column in columns:
					print(self.board[row+column], end = ' ')
				print()
		else:
			for row in rows:
				for column in columns:
					print(self.board[row+column], end = ' ', file = myFile)
				print(file = myFile)


	def setCell(self, cell, value): # will set the value of given cell

		assert(type(value) == str)
		self.board[cell] = value


	def getCell(self, cell): # will return value in specific cell 

		assert((cell[0] in 'ABCDEFGHI') and (cell[1] in '123456789'))
		return self.board[cell]


	def getRow(self, row, exclude = None): # will return list of values in row

		assert(row in 'ABCDEFGHI')

		if exclude == None: # if exclude parameter is passed, get row except exclude
			values = '123456789'
		else:
			values = '123456789'.replace(exclude, '')

		outputRow = []
		for val in values:
			outputRow.append(self.board[row+val])

		return outputRow


	def getColumn(self, column, exclude = None): # will return list of values in column

		assert(column in '123456789')

		if exclude == None: # if exclude parameter is passed, get column except exclude
			values = 'ABCDEFGHI'
		else:
			values = 'ABCDEFGHI'.replace(exclude, '')

		outputColumn = []
		for val in values:
			outputColumn.append(self.board[val+column])

		return outputColumn


	def getBlock(self, blockNum, excludedCell = None, excludeRowCol = False): # will return list of values in block
		
		assert(blockNum in '123456789')

		cells = copy.deepcopy(self.blockMap[blockNum]) # copy of mapping so original isn't modified 
		if excludedCell != None: # if exclude parameter is passed, get block except exclude
			cells.remove(excludedCell)

		cellsCP = copy.deepcopy(cells) # iterate through copy of cells to maintain integrity of iteration
		if excludeRowCol: # if excludeRowCol is True, then remove cells in same column and row as excluded cell
			for cell in cellsCP:
				if (excludedCell[0] in cell) or (excludedCell[1] in cell):
					cells.remove(cell)

		blockVals = []
		for cell in cells:
			blockVals.append(self.board[cell])

		return blockVals


	def findBlock(self, cell): # returns corresponding block number of given cell
		
		for blockNum,cells in self.blockMap.items():
			if cell in cells:
				return blockNum


	def getNeighbors(self, cell): # returns all neighbors of given cell. neighbors = row, column, and block that cell resides in (minus given cell)

		neighbors = set()

		for val in self.getRow(cell[0], cell[1]):
			neighbors.add(val)

		for val in self.getColumn(cell[1], cell[0]):
			neighbors.add(val)

		for val in self.getBlock(self.findBlock(cell), cell):
			neighbors.add(val)

		if '0' in neighbors: neighbors.remove('0') # remove zero as it just represents empty space 

		return neighbors


	def getDegree(self, cell): # returns degree of given cell, degree = number of empty spaces in neighbors of given cell

		spaceCount = 0

		for val in self.getRow(cell[0], cell[1]):
			if val == '0': spaceCount += 1
		for val in self.getColumn(cell[1], cell[0]):
			if val == '0': spaceCount += 1
		for val in self.getBlock(self.findBlock(cell), cell, True):
			if val == '0': spaceCount += 1

		return spaceCount


	def getCompliment(self, neighborSet): # returns list conaining compliments of a given set. EX: set([2,4,6,8]) -> [1,3,5,7,9]

		valList = ['1','2','3','4','5','6','7','8','9']
		for val in neighborSet:
			valList.remove(val)

		return valList



class solvePuzzle():

	def __init__(self, sudokuPuzzle = None):

		self.puzzle = sudokuPuzzle
		self.puzzleStack = [] # will hold states of each step in search, invalid states will be poped
		self.triedValues = set()

		#state of current puzzle
		self.solved = False


	def getEmpty(self, puzzle):

		rows = 'ABCDEFGHI'
		columns = '123456789'
		empty = []

		for row in rows:
			for column in columns:
				if puzzle.board[row+column] == '0':
					empty.append(row+column)
		return empty


	def checkDomain(self, puzzle): # will check puzzle for empty domains after forward check and return false if any are empty (no solution)

		for cell in puzzle.puzzleDomains.items():
			if len(cell[1]) == 0: return False

		return True


	def forwardCheckNeighbors(self, puzzle, cellSet): # will check neighbors of cell and remove given val from their domains
		

		for cell in cellSet:
			if len(cell[1]) == 1:
				for cell2 in cellSet:
					if (((cell[0][0] in cell2[0]) or (cell[0][1] in cell2[0])) and (cell[0] != cell2[0])):
						if cell[1][0] in cell2[1]:
							#print(cell2)
							cell2[1].remove(cell[1][0])
							#print("MODIFIED DOMAIN:", end = " ")
							#print(peerCell, end = ' ')
							#print(puzzle.puzzleDomains[peerCell])

		#print("after") # debug
		#print(puzzle.puzzleDomains) # debug



	def forwardCheck(self, puzzle): # updates domain of each empty cell in puzzle based on neighbors

		emptyCellSet = [] # will store the current set of forwarded domains of empty cells in current puzzle
		
		for cell in self.getEmpty(puzzle):
			domain = puzzle.getCompliment(puzzle.getNeighbors(cell))

			emptyCellSet.append((cell,domain))

		#print("before") # debug
		#print(emptyCellSet) # debug

		self.forwardCheckNeighbors(puzzle, emptyCellSet)

		for cell,domain in emptyCellSet:
			puzzle.puzzleDomains[cell] = domain



	def minRemVal(self, puzzle, ignore = False): # will return the cell with the smallest domain size using MRV heuristic
		
		# sort puzzleDomains by length of potential values in cells 
		sortedDomainList = sorted(puzzle.puzzleDomains.items(), key = lambda item : len(item[1]))


		#check for values in domains that have already been tried 
		for cell,domains in sortedDomainList:
			domainsCP = copy.deepcopy(domains)
			for val in domainsCP:
				#if (cell,val) in self.triedValues:
				if (cell, val) in self.puzzleStack[-1].triedVals:
					#print("TRUE")
					domains.remove(val)

		#print(puzzle.triedVals)


		#check for and remove domains that have become empty due to already used values, will skip if ignore flag is true
		if not ignore:
			SDL = copy.deepcopy(sortedDomainList)
			for cell,domains in SDL:
				if len(domains) == 0:
					sortedDomainList.remove((cell,domains))
		

		#if domain becomes completely empty due to removal of tried values return None
		if len(sortedDomainList) == 0:
			print("NO DOMAINS")
			return None


		# store length of shortest cell Domain
		shortestDomainLength = 10
		for cell,domain in sortedDomainList:
			if len(domain) < shortestDomainLength:
				shortestDomainLength = len(domain)

		print("DOMAIN LENGTH = ", end = "")
		print(shortestDomainLength)


		# make sub list of cell domains with shortest length
		minDomains = []


		# add cells and their domains with the shortest length to sub list
		for cell in sortedDomainList:

			#############
			print(cell, end = ' ') # debug 
			print(puzzle.getDegree(cell[0])) # debug
			#############

			if (len(cell[1]) == shortestDomainLength):
				minDomains.append(cell)

		print("MIN DOMAINS")


		#find cell in minDomains with greatest degree
		maxDegree = (None, 0) # (cell location, degree)
		for cell in minDomains: # cell here is (cell, Domain)

			#############
			print(cell, end = ' ') # debug 
			print(puzzle.getDegree(cell[0])) # debug
			#############

			if puzzle.getDegree(cell[0]) >= maxDegree[1]:
				maxDegree = (cell, puzzle.getDegree(cell[0]))

		return maxDegree[0][0]



	def solve(self, file):


		self.puzzleStack.append(sudokuPuzzle(puzzleCopy = self.puzzle, label = 1)) # push beginning puzzle to stack 


		lastCell = None

		while (not self.solved): # or not self.solved):


			if len(self.puzzleStack) == 0: # check to see if puzzle stack is empty, if so there is no global solution to the puzzle
				print("CANNOT SOLVE")
				break


			print("--------------------------") # debug 
			print() # debug
			
			

			currentPuzzle = sudokuPuzzle(puzzleCopy = self.puzzleStack[-1], label = self.puzzleStack[-1].label+1) # grab latest state of puzzle to solve



			self.forwardCheck(currentPuzzle) # forward check the domains of current puzzle

			currentPuzzle.printBoard() # debug
			print()
			print()
			print()


			if (len(currentPuzzle.puzzleDomains) == 0): # check for empty puzzleDomain, if all is empty then puzzle is solved
				self.solved = True
				print()
				currentPuzzle.printBoard(file) # debug
				print()
				print("PUZZLE SOLVED")
				break


			if not self.checkDomain(currentPuzzle): # check domain of current puzzle for any empty, if so then there is no solution to current puzzle
				#self.triedValues.add(lastCell) # add the last cell choice to tried values so we don't pick it again and fail
				currentPuzzle.triedVals.add(lastCell) # test
				self.puzzleStack[-1].triedVals = copy.deepcopy(currentPuzzle.triedVals) #test
				self.puzzleStack.pop()
				print("NO SOLUTION")
				continue
				


			currentCell = self.minRemVal(currentPuzzle) # get cell to assign value to based on the MRV heuristic
			if currentCell == None:
				currentPuzzle.triedVals.add(lastCell) #test
				self.puzzleStack[-1].triedVals = copy.deepcopy(currentPuzzle.triedVals) # test
				self.puzzleStack.pop()
				#self.triedValues.add(lastCell)
				
				
				print("NO MIN VAL")
				continue


			currentVal = currentPuzzle.puzzleDomains[currentCell].pop() # get and remove value from current cell's domain
			currentPuzzle.setCell(currentCell, currentVal) # assign value retrived to current empty cell in current puzzle


			print(currentCell + ' ' + currentVal) # debug

			lastCell = (currentCell, currentVal)
			currentPuzzle.triedVals.add(lastCell) #test

			self.puzzleStack[-1].triedVals = copy.deepcopy(currentPuzzle.triedVals)
			currentPuzzle.puzzleDomains.pop(currentCell) # remove cell from active domain
			self.puzzleStack.append(sudokuPuzzle(puzzleCopy = currentPuzzle)) # add next puzzle state to the stack after assigning cell it's value 



def main():

	#file handling
	file_name = sys.argv[1]
	
	#open file containing puzzle
	sudokuFile = open(file_name+'.txt', "r")
	
	#initialize game board
	sudokuBoard = sudokuPuzzle(sudokuFile)

	#print game board
	sudokuBoard.printBoard()

	#initialize solver obect
	solver = solvePuzzle(sudokuBoard)

	output_file = open(file_name + '_output_.txt', 'w+') #creates output file

	solver.solve(output_file)




if __name__ == "__main__":
	main()