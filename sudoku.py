import time
import sys
import copy
from math import sqrt

#Backtracking Solution without any heuristics
def backtrack(board):
    if not empty_space(board):
        return True
    else:
        row, col = empty_space(board)
    
    for num in range(1, N+1):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if backtrack(board):
                return True

            board[row][col] = 0

    return False

#Bakctracking with MRV heuristic
def backtrackMRV(board):
    if not empty_space(board):
        return True
    else:
        row, col = getMRV(board)

    for num in range(1, N+1):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if backtrackMRV(board):
                return True

            board[row][col] = 0

    return False

def preprocess(board):
    blanks = blank(board)
    blankValues = {}
    for i in blanks:
        pValues = possibleValues(board, i[0], i[1])
        blankValues[i] = pValues
    return blankValues


blankValues = {}
#Forward Checking with MRV Heuristic - CSP
def fwdCheck(board, bk):
    blankValues = bk
    if not empty_space(board):
        return True
    else:
        row, col = getMRV(board)

    blankDomain = copy.deepcopy(blankValues[(row,col)])

    for num in blankDomain:
        tempDomain=copy.deepcopy(blankValues)
        consistent = pruneInvalid(board, row, col, num, blankValues)
        if (consistent==True):
            board[row][col] = num
            result = fwdCheck(board, blankValues)
            if result!=False:
                return True
            
            blankValues = tempDomain
            board[row][col] = 0
    return False

def pruneInvalid(board, row, col, num, blankValues):
    neighbors = getNeighborBlanks(board, row, col)
    for neighborBlank in neighbors:
        neighborDomain = blankValues[neighborBlank]
        if num in neighborDomain:
            blankValues[neighborBlank].remove(num)
            if len(blankValues[neighborBlank])==0:
                return False
    return True

def getNeighborBlanks(board, row, col):    
    neighbors = []
    associatedBlanks = getRowBlanks(board, row) + getColumnBlanks(board, col) + getBoxBlanks(board, row, col)
    for blank in associatedBlanks:
        if blank not in neighbors and blank!=(row,col): 
            neighbors.append(blank)
    return neighbors
    
def getRowBlanks(board, row):
    cells=[]
    for col in range(N):
        if board[row][col]==0:
            cells.append((row, col))
    return cells

def getColumnBlanks(board, col):
    cells=[]
    for row in range(N):
        if board[row][col]==0:    
            cells.append((row,col))
    
    return cells

def getBoxBlanks(board, row, col):       
    cells=[]
    row=(row/int(sqrt(N)))*int(sqrt(N))
    col=(col/int(sqrt(N)))*int(sqrt(N))
    
    for r in range(int(sqrt(N))):
        for c in range(int(sqrt(N))):
            if board[row+r][col+c]==0:
                cells.append((row+r,col+c))
                
    return cells

def getMRV(board):
    q = []
    for i in blank(board):
        possible = possibleValues(board, i[0], i[1])
        q.append((len(possible), i))
    q.sort()
    return q[0][1]


def possibleValues(board, row, col):
    possible = []
    for i in xrange(1, N+1):
        if is_safe(board, row, col, i):
            possible.append(i)
    return possible

def blank(board):
    blanks = []
    for i in xrange(N):
        for j in xrange(N):
            if board[i][j] == 0:
                blanks.append((i, j))
    return blanks

def make_board():
    with open(sys.argv[1], "r") as input_file:
        board = []
        for x in xrange(N):
            row = []
            for num in input_file.readline():
                if num != "\n":
                    row.append(int(num))
            board.append(row)
    return board


def print_board(board):
    if N > 10:
        print board
        return
    print "+-------+-------+-------+"
    for i in range(N):
        print "| {} {} {} | {} {} {} | {} {} {} |".format(*board[i])
        if (i + 1) % int(sqrt(N)) == 0:
            print "+-------+-------+-------+"


def used_in_row(board, row, num):
    for col in range(N):
        if board[row][col] == num:
            return True
    return False


def used_in_col(board, col, num):
    for row in range(N):
        if board[row][col] == num:
            return True
    return False


def used_in_box(board, start_box_row, start_box_col, num):
    for row in range(int(sqrt(N))):
        for col in range(int(sqrt(N))):
            if board[row + start_box_row][col + start_box_col] == num:
                return True
    return False


def is_safe(board, row, col, num):
    if (not used_in_row(board, row, num) and
            not used_in_col(board, col, num) and
            not used_in_box(board, row - row % int(sqrt(N)), col - col % int(sqrt(N)), num)):
        return True
    return False


def empty_space(board):
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                return row, col
    return False

N = 9

if __name__ ==  '__main__':

    if len(sys.argv) != 3:
        print "usage: sudoku.py <puzzle> <N=N, 16, 25...>"
        sys.exit(1)

    N = int(sys.argv[2])
    print "Board Size: %d X %d" % (N, N)
    board = make_board() 
    print "Input:"
    print_board(board)
    print "========================="

    # start = time.time()
    # if backtrack(board):
    #     end = time.time()
    #     print "Plain Backtracking Solution in (" + str(round(end - start, 4)) + " seconds):"
    #     print_board(board)
    # else:
    #     print "No solution exists - Backtracking"

    # board = make_board()
    # start = time.time()
    # if backtrackMRV(board):
    #     end = time.time()
    #     print "Backtracking with Heursitic - MRV - Solution in (" + str(round(end - start, 4)) + " seconds):"
    #     print_board(board)
    # else:
    #     print "No solution exists - Backtracking+MRV"

    board = make_board()
    start = time.time()
    bk = preprocess(board)
    if fwdCheck(board, bk):
        end = time.time()
        print "Forward Checking with MRV Solution in (" + str(round(end - start, 4)) + " seconds):"
        print_board(board)
    else:
        print "No solution exists - Forward Checking"
