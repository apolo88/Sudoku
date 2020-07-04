from Sudoku import *

class DrawInterface:
    def draw_sudoku(self, sudoku: Sudoku):
        print(sudoku.getMatrix())

    def clear_screen(self):
        """Extract text from the currently loaded file."""
        pass