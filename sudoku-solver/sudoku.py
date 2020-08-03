#!/usr/bin/env python
#coding:utf-8
import sys
import time
import copy
import statistics

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    csp = {ROW[r] + COL[c]: [i for i in range(1, 10)] for r in range(9) for c in range(9)}
    neighbors = {ROW[r] + COL[c]: [i for i in range(1, 10)] for r in range(9) for c in range(9)}
    fill(neighbors)
    check_consistent(board, csp, neighbors)
    backtracking_recursive(board, csp)
    
    solved_board = board
    return solved_board

def fill(neighbors):
    for i in range(9):
        for j in range(9):
            values = set()
            for r in range(3):
                for c in range(3):
                    values.add(ROW[r + int(i / 3) * 3] + COL[c + int(j / 3) * 3])
            for c in range(9):
                values.add(ROW[i] + COL[c])
            for r in range(9):
                values.add(ROW[r] + COL[j])

            values.remove(ROW[i] + COL[j])
            neighbors[ROW[i] + COL[j]] = values
            
def check_consistent(board, csp, neighbors):
    for r in range(9):
        for c in range(9):
            val = board[ROW[r] + COL[c]]
            if board[ROW[r] + COL[c]] != 0:
                for n in neighbors[ROW[r] + COL[c]]:
                    if val in csp[n]:
                        csp[n].remove(val)
                csp[ROW[r] + COL[c]] = [val]
                
def backtracking_recursive(board, csp):
    r = -1
    c = -1
    for i in range(9):
        for j in range(9):
            if board[ROW[i] + COL[j]] == 0: # Finding location of empty cells
                r = i
                c = j               
    if r == -1:
        return True # Done
    
    r, c = mrv(board, csp)
    csp_for_backtracking = copy.deepcopy(csp)
    for val in range(1, 10):
        if satisfies(board, r, c, val):
            board[ROW[r] + COL[c]] = val
            result = update(csp, r, c, val)
            if result != -1:
                if backtracking_recursive(board, csp):
                    return True
            csp = csp_for_backtracking # Backtracking
            board[ROW[r] + COL[c]] = 0 # Backtracking
    return False 

def mrv(board, csp):
    minimum_row = -1
    minimum_col = -1 
    length = 9999 
    for r in range(9):
        for c in range(9):
            if board[ROW[r] + COL[c]] == 0:
                if len(csp[ROW[r] + COL[c]]) < length:
                    minimum_row = r
                    minimum_col = c
                    length = len(csp[ROW[r] + COL[c]])
    return minimum_row, minimum_col

def satisfies(board, r, c, val):
    for row in range(3): # Checks box
        for col in range(3):
            if board[ROW[row + int(r / 3) * 3] + COL[col + int(c / 3) * 3]] == val:
                return False
                
    for col in range(9): # Checks row
        if board[ROW[r] + COL[col]] == val:
            return False
            
    for row in range(9): # Checks column
        if board[ROW[row] + COL[c]] == val:
            return False
    
    return True

def update(csp, r, c, val):
    for row in range(3):
        for col in range(3):
            if val in csp[ROW[row + int(r / 3) * 3] + COL[col + int(c / 3) * 3]]:
                csp[ROW[row + int(r / 3) * 3] + COL[col + int(c / 3) * 3]].remove(val)
                
    for col in range(9):
        if val in csp[ROW[r] + COL[col]]:
            csp[ROW[r] + COL[col]].remove(val)

    for row in range(9):
        if val in csp[ROW[row] + COL[c]]:
            csp[ROW[row] + COL[c]].remove(val)
    
    csp[ROW[r] + COL[c]] = [val] # Adds value back
    
    for row in range(9):
        for col in range(9):
            if len(csp[ROW[row] + COL[col]]) == 0:
                return False 
    return True


if __name__ == '__main__':

    if len(sys.argv) > 1:

        #  Read individual board from command line arg.
        sudoku = sys.argv[1]

        if len(sudoku) != 81:
            print("Error reading the sudoku string %s" % sys.argv[1])
        else:
            board = { ROW[r] + COL[c]: int(sudoku[9*r+c])
                      for r in range(9) for c in range(9)}
            
            print_board(board)

            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()

            print_board(solved_board)

            out_filename = 'output.txt'
            outfile = open(out_filename, "w")
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

    else:

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        '''
        results_filename = 'README.txt' # Setting up README.txt
        results_file = open(results_filename, "w") 
        boards_solved = 0
        running_times = []
        '''

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                    for r in range(9) for c in range(9)}

            # Print starting board.
            print_board(board)

            # Solve with backtracking
            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()
            '''
            running_times.append(end_time - start_time) # Adding each board's running time to list
            '''

            # Print solved board. 
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        '''
        # Checking how many boards in my output match boards in sudokus_finish.txt
        with open('output.txt') as actual, open('sudokus_finish.txt') as expected:
            for line_actual, line_expected in zip(actual, expected):
                if line_actual.strip() == line_expected.strip():
                    boards_solved += 1
                    
        results_file.write("Number of boards solved: " + str(boards_solved) + "\n")                  
        results_file.write("Minimum running time: " + str("%.8f" % min(running_times)) + " seconds\n") 
        results_file.write("Maximum running time: " + str("%.8f" % max(running_times)) + " seconds\n")
        results_file.write("Mean running time: " + str("%.8f" % statistics.mean(running_times)) + " seconds\n")
        results_file.write("Standard deviation of running times: " + str("%.8f" % statistics.stdev(running_times)) + " seconds\n")
        '''
        
        print("Finishing all boards in file.")
