#from DrawInterface import *

class Sudoku:
    rows, cols = 9, 9
    matrix = 0

    def __init__(self, filePath):
        print("Init Sudoku")

        self.matrix = [[0 for x in range(self.rows)] for y in range(self.cols)]
        
        f = open(filePath, "r")
        for row in range (0,self.rows):  
            line = f.readline().strip().replace(' ','')
            for col in range (0,self.cols):
            #for letter in line:
                #print(letter)
                #print(line[col])
                self.matrix[row][col] = line[col]

    def getMatrix(self):
        return self.matrix