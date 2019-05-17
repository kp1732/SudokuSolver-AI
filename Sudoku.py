from __future__ import print_function

class sudokuPuzzle():

	def __init__(self, file = None):

		self.board = {}
		if file != None:
			self.fillBoard(file)

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


	def printBoard(self): # unfinished

		rows = 'ABCDEFGHI'
		columns = '123456789'

		#loop through board and print 
		for row in rows:
			for column in columns:
				print(self.board[row+column], end = ' ')
			print()


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


	def getBlock(self, blockNum, exclude = None): # will return list of values in block
		
		assert(blockNum in '123456789')

		cells = self.blockMap[blockNum]
		if exclude != None: # if exclude parameter is passed, get block except exclude
			cells.remove(exclude)

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


class solvePuzzle():

	def __init__(self, sudokuPuzzle = None):

		self.puzzle = sudokuPuzzle
		self.solved = False
		self.puzzleDomains = {}


	def getCompliment(self, neighborSet): # returns list conaining compliments of a given set. EX: set([2,4,6,8]) -> [1,3,5,7,9]

		valList = ['1','2','3','4','5','6','7','8','9']
		for val in neighborSet:
			valList.remove(val)

		return valList

	
	def updateDomains(self): # updates domain of each empty cell in puzzle based on neighbors
		
		rows = 'ABCDEFGHI'
		columns = '123456789'

		#loop through board and update domains of all locaitons
		for row in rows:
			for column in columns:
				if self.puzzle.board[row+column] == '0':
					
					domain = self.getCompliment(self.puzzle.getNeighbors(row+column))
					self.puzzleDomains[row+column] = domain

		return self.puzzleDomains


#prints item in dictionary sorted by key, mostly for debug
def myPrint(dictionary):
	for key,value in sorted(dictionary.items(), key = lambda item : len(item[1])):
		print(key + " " + str(value))


def main():
	
	#open file containing puzzle
	sudokuFile = open("SUDUKO_Input1.txt", "r")
	
	#initialize game board
	sudokuBoard = sudokuPuzzle(sudokuFile)

	#print game board
	#sudokuBoard.printBoard()

	#get cell
	#print(sudokuBoard.getCell('H8'))

	#get row
	#print(sudokuBoard.getRow('F', '6'))

	#get column
	#print(sudokuBoard.getColumn('1', 'D'))

	#get block 
	#print(sudokuBoard.getBlock('1', 'B2'))

	#get neighbors
	#print(sudokuBoard.getNeighbors('A1'))

	#initialize solvePuzzle class with sudoku puzzle
	#solver = solvePuzzle(sudokuBoard)
	#myPrint(solver.updateDomains())


if __name__ == "__main__":
	main()
