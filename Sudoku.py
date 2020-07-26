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
                print("look for alayze tech pos")
            
                self.analyzeTechPos()
            #    continue
            #    pass

            self.draw_sudoku()
            sys.stdin.read(1)


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
                    print("Block %i Row %i pos values in the row %s " % (block, row, str(posValues)))
                    self.removePossibleValuesRow(row, self.colsByBlock.get(block), posValues)

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
                    print("Block %i Col %i pos values in the col %s " % (block, col, str(posValues)))
                    self.removePossibleValuesCol(self.rowsByBlock.get(block), col, posValues)

            
            
            
            # create list of unfilled positions with the possible values
            # put them in a map by row and col inside the block only the values that are unique in that row or col

            

            #loop the rows and cols just assigned and call the methods to remove possibilities 
            #for row in techPosByRow.keys():
            #    self.removePossibleValuesRow(row, self.colsByBlock.get(block), techPosByRow.get(row))

            print("Block %i analyzed" % block)
            #for col in techPosByCol.keys():
            #    removePossibleValuesCol(self.rowsByBlock.get(block), col, techPosByRow.get(col))


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
        self.removePossibleValuesBlock(row, col, blockNumber, num)


    def removePossibleValuesRow(self, row, currentCols, nums):
        for col in set([0,1,2,3,4,5,6,7,8]) - set(currentCols):
            key = str(row)+str(col)
            for num in nums:
                if key in self.unfilledPosValues and num in self.unfilledPosValues[key]:
                    self.unfilledPosValues[key].remove(num)


    def removePossibleValuesCol(self, currentRows, col, nums):
        for row in set([0,1,2,3,4,5,6,7,8]) - set(currentRows):
            key = str(row)+str(col)
            for num in nums:
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
        print("missing values: %i" % len(self.unfilledPosValues))


    def save_to_file(self):
        result = self.get_text_matrix()

        f = open("files/sudokuSolution.txt", "w")
        f.write(result)
        f.close()