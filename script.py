from Sudoku import *
from DrawConsoleImpl import *

def main():    
    draw = DrawConsoleImpl()
    
    sudoku = Sudoku("files/sudokuToVerify.txt");
    #print(sudoku.getMatrix())
    draw.draw_sudoku(sudoku)

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()