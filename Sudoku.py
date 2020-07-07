#from DrawConsoleImpl import *
import sys

class Sudoku:
    
    class Coord:
        x = 0
        y = 0

        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    """class Pos:
        value = 0
        isPreDef = False

        def __init__(self, value, isPreDef):
            self.value = value
            self.isPreDef = isPreDef"""

    #Attributes
    blocksIdMap = {'0,0':0, '0,1':1, '0,2':2, '1,0':3, '1,1':4, '1,2':5, '2,0':6, '2,1':7, '2,2':8}
    blocksMap = {0:Coord(0,0), 1:Coord(0,3), 2:Coord(0,6), 3:Coord(3,0), 4:Coord(3,3), 5:Coord(3,6), 6:Coord(6,0), 7:Coord(6,3), 8:Coord(6,6)}
    dim = 9
    matrix = 0
    unfilledValues = 0

    def __init__(self, filePath):
        #opens the file and parses the file and complete de matrix
        f = open(filePath, "r")
        self.completeMatrix(f)
        
        #closes the file
        f.close()    

    def completeMatrix(self, f):
        self.matrix = [[0 for x in range(self.dim)] for y in range(self.dim)]
        for row in range (0,self.dim):  
            line = f.readline().strip().replace(' ','')
            for col in range (0,self.dim):
                self.matrix[row][col] = line[col]

                if self.matrix[row][col] == 'n':
                    self.unfilledValues = self.unfilledValues + 1


    def verify(self):
        #check rows
        for i in range (0, self.dim):
            if not(self.verifyRow(i)) or not(self.verifyCol(i)) or not(self.verifyBlock(i)):
                return False
        
        return True


    def verifyRow(self, row):
        filledNumber = set()
        for col in range (0, self.dim):
            if self.matrix[row][col] != 'n':
                filledNumber.add(self.matrix[row][col])

        if(len(filledNumber) != 9):
            print("row %i, diff: %i " % (row, len(filledNumber)))
            return False
        else:
            return True


    def verifyCol(self, col):
        filledNumber = set()
        for row in range (0, self.dim):
            if self.matrix[row][col] != 'n':
                filledNumber.add(self.matrix[row][col])

        if(len(filledNumber) != 9):
            print("col %i, diff: %i " % (col, len(filledNumber)))
            return False
        else:
            return True


    def verifyBlock(self, block):
        coord = self.blocksMap.get(block)
        
        filledNumber = set()
        for row in range (coord.x, coord.x + 3):
            for col in range (coord.y, coord.y + 3):
                if self.matrix[row][col] != 'n':
                    filledNumber.add(self.matrix[row][col])

        if(len(filledNumber) != 9):
            print("block %i, diff: %i " % (block, len(filledNumber)))
            return False
        else:
            return True


    def solve(self):
        self.draw_sudoku()
        sys.stdin.read(1)

        while self.unfilledValues > 0:
            for row in range (0,self.dim):  
                for col in range (0,self.dim):
                    if self.matrix[row][col] == 'n':
                        if self.completePosition(row, col):
                            self.unfilledValues = self.unfilledValues - 1
                            print("missing values: %i" % self.unfilledValues)
                    
            self.draw_sudoku()
            sys.stdin.read(1)


    def completePosition(self, x, y):
        if self.bruteForceMet(x, y):
            return True


    def bruteForceMet(self, x, y):
        numsToVerify = set()
        numsToVerify.update(self.getRowValues(x))
        numsToVerify.update(self.getColValues(y))
        numsToVerify.update(self.getBlockValues(self.getBlockNumber(x,y)))

        if len(numsToVerify) == 8:
            leftNumbers = set(['1','2','3','4','5','6','7','8','9'])
            for i in numsToVerify:
                leftNumbers.remove(i)

            numToFill = leftNumbers.pop()
            self.matrix[x][y] = numToFill

            print("BruteForce: value %s in row %i col %i" % (numToFill, x, y))

            return True
        else:
            return False


    def getRowValues(self, row):
        rowValues = set()

        for col in range (0, self.dim):
            if self.matrix[row][col] != 'n':
                rowValues.add(self.matrix[row][col])

        return rowValues


    def getColValues(self, col):
        colValues = set()

        for row in range (0, self.dim):
            if self.matrix[row][col] != 'n':
                colValues.add(self.matrix[row][col])

        return colValues


    def getBlockValues(self, block):
        coord = self.blocksMap.get(block)

        blockValues = set()
        for row in range (coord.x, coord.x + 3):
            for col in range (coord.y, coord.y + 3):
                if self.matrix[row][col] != 'n':
                    blockValues.add(self.matrix[row][col])
        
        return blockValues


    def getBlockNumber(self, row, col):
        return self.blocksIdMap.get(str(row//3) + ',' + str(col//3))


    def get_text_matrix(self) -> str:
        rows, cols = 9, 9
        
        result = ''
        for row in range (0,rows):  
            if row % 3 == 0:
                result += '-------------------\n'
            
            if row % 3 == 1 or row % 3 == 2:
                result += '|     |     |     |\n'

            line = ''
            for col in range (0,cols):
                if col % 3 == 0:
                    line += '|'
                
                line += self.matrix[row][col]

                if col % 3 == 0 or col % 3 == 1:
                    line += ' '

            line += '|'

            result += line + '\n'
        
        result += '-------------------'
        
        return result


    def draw_sudoku(self): 
        print(self.get_text_matrix())
        print("missing values: %i" % self.unfilledValues)          


    def save_to_file(self):
        result = self.get_text_matrix()
        #print(result)

        f = open("files/sudokuSolution.txt", "w")
        f.write(result)
        f.close()