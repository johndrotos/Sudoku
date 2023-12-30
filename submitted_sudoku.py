#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import copy
import time

ROW = "ABCDEFGHI"
COL = "123456789"

global_board = { ROW[r] + COL[c]: 0
                  for r in range(9) for c in range(9)}    


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

#def arc_consistency(board):
    
    
def b_copy(board):
    #manually deep copies the board
    board_copy = {}
    for key in board:
        i = board[key]
        board_copy[key] = i
    return board_copy
        
def d_copy(domains):
    domains_copy = {}
    for key in domains:
        domains_copy[key] = domains[key].copy()
    return domains_copy


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    
    # Checks if the board is already complete
    is_complete = True
    for value in board.values():
        if value == 0:
            is_complete = False
    if is_complete:
        return board
    
    
    #creating a dictionary for the domains
    domains = { ROW[r] + COL[c]: [1,2,3,4,5,6,7,8,9]
                      for r in range(9) for c in range(9)}
    
    for key in domains:
        if board[key] != 0:
            domains[key] = []
            domains[key].append(0)
            
                
    box1 = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
    box2 = ["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"]
    box3 = ["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"]
    box4 = ["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"]
    box5 = ["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"]
    box6 = ["D7", "D8", "D9", "E7", "E8", "E9", "F7", "F8", "F9"]
    box7 = ["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"]
    box8 = ["G4", "G5", "G6", "H4", "H5", "H6", "I4", "I5", "I6"]
    box9 = ["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]
    boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9]
    
    for r in ROW:
        for c in COL:
            if len(domains[r+c]) > 1:
                #checks the row
                for i in range(9):
                    if board[r + COL[i]] in domains[r+c]:
                        domains[r+c].remove(board[r+COL[i]])
                #checks the column
                for i in ROW:
                    if board[i+c] in domains[r+c]:
                        domains[r+c].remove(board[i+c])
                #checks the box
                for box in boxes:
                    if r+c in box:
                        for square in box:
                            if board[square] in domains[r+c]:
                                domains[r+c].remove(board[square])
                            
    backtrack_recursion(board, domains, boxes)
        
    
    #solved_board = b_copy(global_board)
    return global_board



def backtrack_recursion(board, domains, boxes):
    #checks if solved
    is_complete = True
    for value in board.values():
        if value == 0:
            is_complete = False
    if is_complete:
        global global_board
        global_board = b_copy(board)
        return True
    
    #finds mrv
    mrv = "A1"
    for key in domains:
        if board[key] == 0 and domains[key][0] != 0:
            if len(domains[key]) < len(domains[mrv]) or domains[mrv] == [0]:
                mrv = key    
    
    #assigns a value to mrv
    
    for i in domains[mrv]:
        board_copy = b_copy(board)
        domains_copy = d_copy(domains)
        if forward_check(board, domains, mrv, boxes, i) == True:
            board_copy[mrv] = i
            domains_copy[mrv] = []
            domains_copy[mrv].append(0)
            
            domain_prune(board_copy, domains_copy, boxes)
            if backtrack_recursion(board_copy, domains_copy, boxes):
                return True
    return False
            
            
            
#helper functions

"""def domain_revert(board, domains, boxes, square, value):
    r = square[0]
    c = square[1]
    #checks the row
    for i in COL:
        if i != c:
            domains[r+c].append(value)
    #checks the column
    for i in ROW:
        if i != r:
            domains[r+c].append(value)
    #checks the box
    for box in boxes:
        if r+c in box:
            for square in box:
                if square != (r+c):
                    domains[r+c].append(value)"""
        
    

def domain_prune(board, domains, boxes):
    for r in ROW:
        for c in COL:
            if len(domains[r+c]) > 1:
                #checks the row
                for i in range(9):
                    if board[r+COL[i]] in domains[r+c]:
                        domains[r+c].remove(board[r+COL[i]])
                #checks the column
                for i in ROW:
                    if board[i+c] in domains[r+c]:
                        domains[r+c].remove(board[i+c])
                #checks the box
                for box in boxes:
                    if r+c in box:
                        for square in box:
                            if board[square] in domains[r+c]:
                                domains[r+c].remove(board[square])

"""def consistency_check(board, square, boxes, potential_value):
    r = square[0]
    c = square[1]
    for i in COL:
        if board[r+i] == potential_value and i != c:
            return False
    for i in ROW:
        if board[i+c] == potential_value and i != r:
            return False
    for box in boxes:
        if r+c in box:
            for square1 in box:
                if board[square1] == potential_value and square1 != square:
                    return False
    return True"""


def forward_check(board, domains, mrv, boxes, potential_value):
    domains_copy = {}
    for key in domains:
        domains_copy[key] = domains[key].copy()
    r = mrv[0]
    for i in COL:
        if board[r+i] == potential_value and i != c:
            return False
        elif potential_value in domains_copy[r+i] and mrv != (r+i):
            domains_copy[r+i].remove(potential_value)
            if len(domains_copy[r+i]) == 0:
                return False
    c = mrv[1]
    for i in ROW:
        if board[i+c] == potential_value and i != r:
            return False
        elif potential_value in domains_copy[i+c] and mrv != (i+c):
            domains_copy[i+c].remove(potential_value)
            if len(domains_copy[i+c]) == 0:
                return False
    for box in boxes:
        if r+c in box:
            for square1 in box:
                if board[square1] == potential_value and square1 != mrv:
                    return False
        elif r+c in box:
            for square in box:
                if potential_value in domains_copy[square] and mrv != square:
                    domains_copy[square].remove(potential_value)
                    if len(domains_copy[square]) == 0:
                        return False
    return True




if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'test.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        times = []

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            
     

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)
            
            start_time  = time.time()

            # Solve with backtracking
            solved_board = backtracking(board)


            end_time = time.time()
            
            times.append(end_time - start_time)

            # Print solved board. TODO: Comment this out when timing runs.
            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        #time stats
        #min
        min = times[0]
        for time in times:
            if time < min:
                min = time
        #max
        max = times[0]
        for time in times:
            if time > max:
                max = time
        
        #mean
        mean = 0
        for time in times:
            mean += time
        mean = mean/len(times)
        
        #standard deviation
        std_dev = 0
        for time in times:
            std_dev += (time - mean)**2
        std_dev = std_dev/len(times)
        std_dev = std_dev**(1/2)
        
        print("min: " + str(min))
        print("max: " + str(max))
        print("mean: " + str(mean))
        print("std_dev: " + str(std_dev))
        
        
        print("Finishing all boards in file.")