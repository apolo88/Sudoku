from Sudoku import *
import sys

def main():    
    #validates the file solution and checks if it is correct or not
    #verifySudokuSolution()

    #solves the sudoku on the file to solve and saves it in the solution file
    solveSudoku()

def verifySudokuSolution():
    sudoku = Sudoku("files/sudokuToVerify.txt")
    sudoku.draw_sudoku()
    sys.stdin.read(1)
    print(sudoku.verify())

def clear_screen(self):
    """Extract text from the currently loaded file."""
    pass

def solveSudoku():
    sudoku = Sudoku("files/sudokuToSolve.txt")
    sudoku.solve()

    print("Sudoku correct : %s" % sudoku.verify())
    #sudoku.draw_sudoku()
    #sudoku.save_to_file()

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()