#from DrawConsoleImpl import *
import sys

class Sudoku:
    
    class Coord:
        x = 0
        y = 0

        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    #General Attributes
    dim = 9
    blocksIdMap = {'00':0, '01':1, '02':2, '10':3, '11':4, '12':5, '20':6, '21':7, '22':8}

    matrix = 0
    blockStartCordMap = {0:Coord(0,0), 1:Coord(0,3), 2:Coord(0,6), 3:Coord(3,0), 4:Coord(3,3), 5:Coord(3,6), 6:Coord(6,0), 7:Coord(6,3), 8:Coord(6,6)}
    colsToAnalyzeByBlock = {0:[0,1,2], 1:[3,4,5], 2:[6,7,8], 3:[0,1,2], 4:[3,4,5], 5:[6,7,8], 6:[0,1,2], 7:[3,4,5], 8:[6,7,8]}
    rowsToAnalyzeByBlock = {0:[0,1,2], 1:[0,1,2], 2:[0,1,2], 3:[3,4,5], 4:[3,4,5], 5:[3,4,5], 6:[6,7,8], 7:[6,7,8], 8:[6,7,8]}
    blocksToAnalyzeByRow = {0:[0,1,2], 1:[0,1,2], 2:[0,1,2], 3:[3,4,5], 4:[3,4,5], 5:[3,4,5], 6:[6,7,8], 7:[6,7,8], 8:[6,7,8]}
    blocksToAnalyzeByCol = {0:[0,3,6], 1:[1,4,7], 2:[2,5,8], 3:[0,3,6], 4:[1,4,7], 5:[2,5,8], 6:[0,3,6], 7:[1,4,7], 8:[2,5,8]}

    # key of the position (RowCol) and the set of possible values
    unfilledPosValues = {}
    unfilledPosKeysByBlock = {}

    #Constructor
    def __init__(self, filePath):
        #opens the file and parses the file and complete de matrix
        f = open(filePath, "r")
        self.completeMatrix(f)
        
        #closes the file
        f.close()    


    #Fill the matrix with the file
    def completeMatrix(self, f):
        self.matrix = [[0 for x in range(self.dim)] for y in range(self.dim)]
        for row in range (0,self.dim):  
            line = f.readline().strip().replace(' ','')
            for col in range (0,self.dim):
                self.matrix[row][col] = line[col]

                if self.matrix[row][col] == 'n':
                    # loads that unfilled position to the correct block
                    blockNumber = self.getBlockNumber(row,col)
                    if blockNumber in self.unfilledPosKeysByBlock:
                        self.unfilledPosKeysByBlock[blockNumber].append(str(row) + str(col))
                    else:
                        self.unfilledPosKeysByBlock[blockNumber] = [str(row) + str(col)]

      
    def getBlockNumber(self, row, col):
        return self.blocksIdMap.get(str(row//3) + str(col//3))


    ############################################
    ############################################
    ### VALIDATION
    ############################################
    ############################################

    #Validates if a sudoku is valid or not
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
        coord = self.blockStartCordMap.get(block)
        
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


    ############################################
    ############################################
    ### RESOLUTION
    ############################################
    ############################################


    #init method to solve the sudoku
    def solve(self):
        self.draw_sudoku()
        sys.stdin.read(1)

        # loops again all the positions if they were not solved yet
        while len(self.unfilledPosKeysByBlock) > 0:

            dictKeys = self.unfilledPosKeysByBlock.copy().keys()
            for block in dictKeys:
                
                #TODO deep dive on why seems to work more performant with copy
                self.checkDiscardAndFillPosValues(self.unfilledPosKeysByBlock[block].copy())

                # checks after first validation if there are still items to complete in the block
                if block in self.unfilledPosKeysByBlock:
                    self.checkParallelsMethod(self.unfilledPosKeysByBlock[block])

            self.draw_sudoku()
            sys.stdin.read(1)


    ############################################
    ############################################
    ### RESOLUTION ALGORITHMS
    ############################################
    ############################################



    ### DISCARD METHOD

    def checkDiscardAndFillPosValues(self, unfilledPos):
        for key in unfilledPos:
            if key not in self.unfilledPosValues:
                self.unfilledPosValues[key] = self.getPosValues(int(key[0]), int(key[1]))

            if len(self.unfilledPosValues[key]) == 1:
                self.fillNumber(int(key[0]), int(key[1]), self.unfilledPosValues[key].pop(), "Discard")


    
    ### CHECK PARALLELS METHOD

    def checkParallelsMethod(self, unfilledPos):
        for key in unfilledPos:
            row = int(key[0])
            col = int(key[1])

            blockNumber = self.getBlockNumber(row,col)

            #for each possible number
            candValue = -1
            for num in self.unfilledPosValues[str(row) + str(col)]:
                print("cords: %s analyzing %i" % (str(row) + str(col), int(num)))
                if (self.validForParallelPerRow(row, col, num, blockNumber) and self.verifyNumberPerBlockRow(num, row, blockNumber)) or (self.validForParallelPerCol(row, col, num, blockNumber) and self.verifyNumberPerBlockCol(num, col, blockNumber)):
                    candValue = int(num)
                    break
                
            if candValue >= 0:
                self.fillNumber(row, col, num, "Parallel")


    def validForParallelPerRow(self, row, col, num, blockNumber):
        for altCol in set(self.colsToAnalyzeByBlock[blockNumber]) - set([col]):
            #print("altCol %s" % altCol)
            if self.matrix[row][altCol] == 'n' and num in self.unfilledPosValues[str(row) + str(altCol)]:
                return False

        #print("validRow")
        return True

    #TODO Review method, calculating wrong
    def validForParallelPerCol(self, row, col, num, blockNumber):
        for altRow in set(self.rowsToAnalyzeByBlock[blockNumber]) - set([row]):
            #print("altRow %s" % altRow)
            #if self.matrix[altRow][col] == 'n':
                #print(str(self.unfilledPosValues))
            if self.matrix[altRow][col] == 'n' and num in self.unfilledPosValues[str(altRow) + str(col)]:
                return False

        print("validCol")
        return True

    def verifyNumberPerBlockRow(self, num, currentRow, currentBlock):
        #loop resting blocks in the same row
        for block in set(self.blocksToAnalyzeByRow[currentBlock]) - set([currentBlock]):
            found = False
            coord = self.blockStartCordMap.get(block)
            for row in set([coord.x, coord.x + 1, coord.x + 2]) - set([currentRow]):
                for col in range (coord.y, coord.y + 3):
                    if self.matrix[row][col] == num:
                        found = True
                        break;

            if not found:
                return False

        print("number applied per row")
        return True

    #Review method, calculating wrong 
    def verifyNumberPerBlockCol(self, num, currentCol, currentBlock):
        #loop resting blocks in the same row
        for block in set(self.blocksToAnalyzeByCol[currentBlock]) - set([currentBlock]):
            found = False
            coord = self.blockStartCordMap.get(block)
            for row in range (coord.x, coord.x + 3):
                for col in set([coord.y, coord.y + 1, coord.y + 2]) - set([currentCol]):
                    if self.matrix[row][col] == num:
                        found = True
                        break;

            if not found:
                return False

        print("number applied per col")
        return True

    #####################################################
    ### Complete cell and recalculate possible Values ###
    #####################################################

    def fillNumber(self, row, col, num, meth):
        self.matrix[row][col] = num

        print("Number filled, Row %s Col %s Value %s with Method: %s" % (row, col, num, meth))

        #removes key from the unfilled values map
        del self.unfilledPosValues[str(row) + str(col)]

        # removes position from the blocks map
        blockNumber = self.getBlockNumber(row,col)
        self.unfilledPosKeysByBlock[blockNumber].remove(str(row) + str(col))

        self.removePossibleValues(row, col, blockNumber, num)

        #TODO analyze to call recursively to fillNumber if the left number is one
        #if len(self.unfilledPosValues[str(row) + str(col)]) == 1:
            #self.fillNumber(row, col, posNumbers.pop(), "Discard")

        # if the last item was removed then removes the entire block
        if len(self.unfilledPosKeysByBlock[blockNumber]) == 0:
            del self.unfilledPosKeysByBlock[blockNumber]


    def removePossibleValues(self, row, col, blockNumber, num):
        self.removePossibleValuesRow(row, col, num)
        self.removePossibleValuesCol(row, col, num)
        self.removePossibleValuesBlock(row, col, blockNumber, num)


    def removePossibleValuesRow(self, row, currentCol, num):
        for col in set([0,1,2,3,4,5,6,7,8]) - set([currentCol]):
            key = str(row)+str(col)
            if key in self.unfilledPosValues and num in self.unfilledPosValues[key]:
                self.unfilledPosValues[key].remove(num)


    def removePossibleValuesCol(self, currentRow, col, num):
        for row in set([0,1,2,3,4,5,6,7,8]) - set([currentRow]):
            key = str(row)+str(col)
            if key in self.unfilledPosValues and num in self.unfilledPosValues[key]:
                self.unfilledPosValues[key].remove(num)


    def removePossibleValuesBlock(self, currentRow, currentCol, blockNumber, num):
        coord = self.blockStartCordMap.get(blockNumber)
        for row in range (coord.x, coord.x + 3):
            for col in range (coord.y, coord.y + 3):
                if currentRow != row or currentCol != col:
                    key = str(row)+str(col)
                    if key in self.unfilledPosValues and num in self.unfilledPosValues[key]:
                        self.unfilledPosValues[key].remove(num)


    #####################################################
    ### Possible Values Analysis ####
    #####################################################


    def getPosValues(self, x, y):
        numsToVerify = set()
        numsToVerify.update(self.getRowValues(x))
        numsToVerify.update(self.getColValues(y))
        numsToVerify.update(self.getBlockValues(self.getBlockNumber(x,y)))

        return set(['1','2','3','4','5','6','7','8','9']) - numsToVerify


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
        coord = self.blockStartCordMap.get(block)

        blockValues = set()
        for row in range (coord.x, coord.x + 3):
            for col in range (coord.y, coord.y + 3):
                if self.matrix[row][col] != 'n':
                    blockValues.add(self.matrix[row][col])
        
        return blockValues

   
    ############################################
    ############################################
    ### PRINTING
    ############################################
    ############################################


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
        #print("missing values: %i" % self.unfilledValues)          
        print("missing values: %i" % len(self.unfilledPosValues))


    def save_to_file(self):
        result = self.get_text_matrix()
        #print(result)

        f = open("files/sudokuSolution.txt", "w")
        f.write(result)
        f.close()