import sys
import math
import copy

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
    deepLevel = 0

    matrix = [[]]
    blockStartCordMap = {0:Coord(0,0), 1:Coord(0,3), 2:Coord(0,6), 3:Coord(3,0), 4:Coord(3,3), 5:Coord(3,6), 6:Coord(6,0), 7:Coord(6,3), 8:Coord(6,6)}
    rowsByBlock = {0:[0,1,2], 1:[0,1,2], 2:[0,1,2], 3:[3,4,5], 4:[3,4,5], 5:[3,4,5], 6:[6,7,8], 7:[6,7,8], 8:[6,7,8]}
    colsByBlock = {0:[0,1,2], 1:[3,4,5], 2:[6,7,8], 3:[0,1,2], 4:[3,4,5], 5:[6,7,8], 6:[0,1,2], 7:[3,4,5], 8:[6,7,8]}

    # key of the position (RowCol) and the set of possible values
    unfilledPosValues = {}


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
                    self.unfilledPosValues[str(row) + str(col)] = set()

      
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

        # Loads all poss values and fills in case is only one number
        self.loadPosValues()
        self.deepSolve()


    def deepSolve(self):
        # Iterate the unifilledPos to complete them
        while len(self.unfilledPosValues) > 0:
            unfilledPosBeforeProcess = len(self.unfilledPosValues)
            for key in self.unfilledPosValues.copy().keys():
                if key in self.unfilledPosValues:
                    #looks if it has only one pos value
                    if self.checkDiscard(key):
                        continue

                    #analyze the different possibilities of unique pos Value per block, row and col
                    if self.checkUniquePosValueInters(key):
                        continue

            if unfilledPosBeforeProcess == len(self.unfilledPosValues):
                print("analyze tech pos")
                if self.analyzeTechPos():
                    continue

                print("analyze preemptive sets")
                if self.analyzePreemptiveSets():
                    continue

                print("analyze tree decision")    
                if not self.analyzeTreeDecision():
                    print("No way to continue.")
                    break;

            print("Deep level: %i" % self.deepLevel)
            self.draw_sudoku()
            sys.stdin.read(1)

        return len(self.unfilledPosValues) == 0


    def loadPosValues(self):
        for key in self.unfilledPosValues.keys():
            self.unfilledPosValues[key] = self.getPosValues(int(key[0]), int(key[1]))


    ############################################
    ############################################
    ### RESOLUTION ALGORITHMS
    ############################################
    ############################################


    ### DISCARD METHOD

    def checkDiscard(self, key):
        if len(self.unfilledPosValues[key]) == 1:
            self.fillNumber(int(key[0]), int(key[1]), self.unfilledPosValues[key].pop(), "Discard")
            return True
        else:
            return False
            

    def checkUniquePosValueInters(self, key):
        row = int(key[0])
        col = int(key[1])
        
        candValue = -1
        for num in self.unfilledPosValues[key]:
            if self.isUniquePosValueInBlock(key, row, col, num) or self.isUniquePosValueInRow(key, row, col, num) or self.isUniquePosValueInCol(key, row, col, num):
                candValue = int(num)
                break

        if candValue >= 0:
            self.fillNumber(row, col, num, "Unique Intersection")
            return True
        else:
            return False
        

    def isUniquePosValueInBlock(self, key, currentRow, currentCol, num):
        blockNumber = self.getBlockNumber(currentRow, currentCol)
        coord = self.blockStartCordMap.get(blockNumber)
        
        for row in range (coord.x, coord.x + 3):
            for col in range (coord.y, coord.y + 3):
                if currentRow != row or currentCol != col:
                    posKey = str(row) + str(col)
                    if posKey in self.unfilledPosValues and num in self.unfilledPosValues[posKey]:
                        return False
        
        return True

    
    def isUniquePosValueInRow(self, key, currentRow, currentCol, num):
        for col in set([0,1,2,3,4,5,6,7,8]) - set([currentCol]):
            posKey = str(currentRow) + str(col)
            if posKey in self.unfilledPosValues and num in self.unfilledPosValues[posKey]:
                return False
        
        return True


    def isUniquePosValueInCol(self, key, currentRow, currentCol, num):
        for row in set([0,1,2,3,4,5,6,7,8]) - set([currentRow]):
            posKey = str(row) + str(currentCol)
            if posKey in self.unfilledPosValues and num in self.unfilledPosValues[posKey]:
                return False

        return True


    ### TECH DISCARD METHOD

    def analyzeTechPos(self):
        couldAdvance = False
        for block in self.blockStartCordMap.keys():
            
            coord = self.blockStartCordMap.get(block)      
            
            #fills in map the unique pos values for each row
            for row in range (coord.x, coord.x + 3):
                # get pos values of the row
                posValues = set()            
                for col in range (coord.y, coord.y + 3):
                    if self.matrix[row][col] == 'n':
                        posValues.update(self.unfilledPosValues[str(row)+str(col)])
            
                if len(posValues) == 0:
                    continue

                #loop other rows to mantain only uniques
                for rowAlt in set([coord.x, coord.x + 1, coord.x + 2]) - set([row]):
                    for col in range (coord.y, coord.y + 3):
                        if self.matrix[rowAlt][col] == 'n':
                            posValues.difference_update(self.unfilledPosValues[str(rowAlt)+str(col)])

                #if there are any values found that are uniques for the row then calls the remove logic
                if len(posValues) != 0:
                    couldAdvance = couldAdvance or self.removePossibleValuesRow(row, self.colsByBlock.get(block), posValues)

            #fills in map the unique pos values for each col
            for col in range (coord.y, coord.y + 3):
                # get pos values of the col
                posValues = set()            
                for row in range (coord.x, coord.x + 3):
                    if self.matrix[row][col] == 'n':
                        posValues.update(self.unfilledPosValues[str(row)+str(col)])
            
                if len(posValues) == 0:
                    continue

                #loop other cols to mantain only uniques
                for colAlt in set([coord.y, coord.y + 1, coord.y + 2]) - set([col]):
                    for row in range (coord.x, coord.x + 3):
                        if self.matrix[row][colAlt] == 'n':
                            posValues.difference_update(self.unfilledPosValues[str(row)+str(colAlt)])

                #if there are any values found that are uniques for the row then calls the remove logic
                if len(posValues) != 0:
                    couldAdvance = couldAdvance or self.removePossibleValuesCol(self.rowsByBlock.get(block), col, posValues)

        return couldAdvance


    def analyzePreemptiveSets(self):
        couldAdvance = False
        
        #look for preemptive sets in blocks
        for block in self.blockStartCordMap.keys():
            
            coord = self.blockStartCordMap.get(block)      
            
            #fills in map the unique pos values for each row
            for row in range (coord.x, coord.x + 3):
                for col in range (coord.y, coord.y + 3):
                    if self.matrix[row][col] == 'n':

                        markUpSize = len(self.unfilledPosValues[str(row)+str(col)])
                        preemptivePos = {str(row)+str(col)}

                        #check the other positions to see if matches
                        for rowAux in range (coord.x, coord.x + 3):
                            for colAux in range (coord.y, coord.y + 3):
                                if self.matrix[rowAux][colAux] == 'n':
                                    if rowAux != row or colAux != col:
                                        if self.unfilledPosValues[str(rowAux)+str(colAux)].issubset(self.unfilledPosValues[str(row)+str(col)]):
                                            preemptivePos.add(str(rowAux)+str(colAux))

                        if len(preemptivePos) > 1 and len(preemptivePos) == markUpSize:
                            #remove positions from block
                            couldAdvance = couldAdvance or self.removePossibleValuesBlock(preemptivePos, block, self.unfilledPosValues[str(row)+str(col)])
                            

        #look for preemptive sets in rows
        for row in range (0, 9):
            for col in range (0,9):
                if self.matrix[row][col] == 'n':

                    markUpSize = len(self.unfilledPosValues[str(row)+str(col)])
                    preemptiveColPos = {col}

                    #check the other positions to see if matches
                    for colAux in range (0,9):
                        if self.matrix[row][colAux] == 'n':
                            if colAux != col:
                                if self.unfilledPosValues[str(row)+str(colAux)].issubset(self.unfilledPosValues[str(row)+str(col)]):
                                    preemptiveColPos.add(colAux)

                    if len(preemptiveColPos) > 1 and len(preemptiveColPos) == markUpSize:
                        couldAdvance = couldAdvance or self.removePossibleValuesRow(row, preemptiveColPos, self.unfilledPosValues[str(row)+str(col)])
                        
        #look for preemptive sets in cols
        for col in range (0,9):
            for row in range (0, 9):
                if self.matrix[row][col] == 'n':

                    markUpSize = len(self.unfilledPosValues[str(row)+str(col)])
                    preemptiveRowPos = {row}

                    #check the other positions to see if matches
                    for rowAux in range (0,9):
                        if self.matrix[rowAux][col] == 'n':
                            if rowAux != row:
                                if self.unfilledPosValues[str(rowAux)+str(col)].issubset(self.unfilledPosValues[str(row)+str(col)]):
                                    preemptiveRowPos.add(rowAux)

                    if len(preemptiveRowPos) > 1 and len(preemptiveRowPos) == markUpSize:
                        couldAdvance = couldAdvance or self.removePossibleValuesCol(preemptiveRowPos, col, self.unfilledPosValues[str(row)+str(col)])
           
        return couldAdvance


    def analyzeTreeDecision(self):
        
        targetValues = 2
        # loop unfilled positions looking for one where has only two possible values, in case does not found increments targetValues
        while True:
            #loop positions
            for key in self.unfilledPosValues.keys():
                #if a position has 0 options means the solution didn't go well
                if len(self.unfilledPosValues.get(key)) == 0:
                    return False

                if len(self.unfilledPosValues.get(key)) == targetValues:
                    #for each possible values clones the sudoku considering that value as true and tries to solve it
                    for value in self.unfilledPosValues.get(key):
                        print("Cloning considering Key %s, Value %s" % (key, value))
                        
                        #clone
                        copySudoku = copy.deepcopy(self)
                        copySudoku.matrix = copy.deepcopy(self.matrix)
                        copySudoku.unfilledPosValues = copy.deepcopy(self.unfilledPosValues)
                        copySudoku.deepLevel += 1

                        copySudoku.fillNumber(int(key[0]), int(key[1]), value, "Tree Decision")

                        if copySudoku.deepSolve():
                            print("Solution found by Tree Decision")
                            self.matrix = copy.deepcopy(copySudoku.matrix)
                            self.unfilledPosValues = copy.deepcopy(copySudoku.unfilledPosValues)
                            return True
                            
            targetValues += 1
        


    #####################################################
    ### Complete cell and recalculate possible Values ###
    #####################################################


    def fillNumber(self, row, col, num, meth):
        self.matrix[row][col] = num
        print("Number filled, Row %s Col %s Value %s with Method: %s" % (row, col, num, meth))

        #removes key from the unfilled values map
        del self.unfilledPosValues[str(row) + str(col)]

        # removes filled value from other posValues map in other positions
        self.removePossibleValues(row, col, self.getBlockNumber(row,col), num)


    def removePossibleValues(self, row, col, blockNumber, num):
        self.removePossibleValuesRow(row, [col], [num])
        self.removePossibleValuesCol([row], col, [num])
        self.removePossibleValuesBlock({str(row)+str(col)}, blockNumber, [num])


    def removePossibleValuesRow(self, row, currentCols, nums):
        couldRemove = False
        for col in set([0,1,2,3,4,5,6,7,8]) - set(currentCols):
            key = str(row)+str(col)
            for num in nums:
                if key in self.unfilledPosValues and num in self.unfilledPosValues[key]:
                    self.unfilledPosValues[key].remove(num)
                    couldRemove = True

        return couldRemove


    def removePossibleValuesCol(self, currentRows, col, nums):
        couldRemove = False
        for row in set([0,1,2,3,4,5,6,7,8]) - set(currentRows):
            key = str(row)+str(col)
            for num in nums:
                if key in self.unfilledPosValues and num in self.unfilledPosValues[key]:
                    self.unfilledPosValues[key].remove(num)
                    couldRemove = True
        
        return couldRemove

    
    def removePossibleValuesBlock(self, currentPos, blockNumber, nums):
        couldRemove = False
        coord = self.blockStartCordMap.get(blockNumber)
        for row in range (coord.x, coord.x + 3):
            for col in range (coord.y, coord.y + 3):
                key = str(row)+str(col)
                if key not in currentPos:
                    for num in nums:
                        if key in self.unfilledPosValues and num in self.unfilledPosValues[key]:
                            self.unfilledPosValues[key].remove(num)
                            couldRemove = True

        return couldRemove


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
                result += '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            else:
                result += '-------------------------------------------------------------------------------------------------------------\n'

            result += '|           .           .           |           .           .           |           .           .           |\n'

            line = ''
            for col in range (0,cols):
                if col % 3 == 0:
                    line += '|'
                else:
                    line += '.'
                
                if self.matrix[row][col] != 'n':
                    line += '     ' + self.matrix[row][col] + '     '
                else:
                    blankSpaceQuant = 9 - len(self.unfilledPosValues.get(str(row) + str(col)))
                    
                    for i in range(0, blankSpaceQuant//2):
                        line += ' '
                    
                    line += '('
                    for value in self.unfilledPosValues.get(str(row) + str(col)):
                        line += value
                    line += ')'

                    for i in range(0, math.ceil(blankSpaceQuant/2)):
                        line += ' '

            line += '|'
            result += line + '\n'
            result += '|           .           .           |           .           .           |           .           .           |\n'
        
        result += '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
        
        return result


    def draw_sudoku(self): 
        print(self.get_text_matrix())
        print("missing values: %i" % len(self.unfilledPosValues))


    def save_to_file(self):
        result = self.get_text_matrix()

        f = open("files/sudokuSolution.txt", "w")
        f.write(result)
        f.close()