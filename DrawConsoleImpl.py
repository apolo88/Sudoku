from DrawInterface import *
from Sudoku import *

class DrawConsoleImpl(DrawInterface):
    def draw_sudoku(self, sudoku: Sudoku):
        
        rows, cols = 9, 9
        matrix = sudoku.getMatrix()

        for row in range (0,rows):  
            if(row % 3 == 0)
                print('----------------------')
            for col in range (0,cols):
                if(row % 3 == 0)
                    print('|')
                print(self.matrix[row][col])
                 #= line[col]
        
        #print(sudoku.getMatrix())

    def clear_screen(self):
        """Extract text from the currently loaded file."""
        pass