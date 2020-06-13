"""
Author: Sarthak Padhi   
Email: sarthakpadhi2016@gmail.com
"""


def solve(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for x in range(1, 10):
                    if valid(x, i, j, 9, board ):
                        board[i][j] = x
                        if (solve(board)):
                            return True
                        board[i][j] = 0
                return False
    return True               


def valid(x, row, column, N, board):
    #checkin g in rows by changing column
    for j in range(N):
        if board[row][j] == x:
            return False
    
    #checking in columns by changing rows
    for i in range(N):
        if board[i][column] == x:
            return False
    # for box 
    alpha = 3*(row // 3)
    beta = 3*(column // 3)
    for i in range(alpha, alpha + 3):
        for j in range(beta, beta + 3):
            if board[i][j] == x:
                return False

    return True   

def printBoard(board):   
    for i in board:
        print(i) 
    print("---------------------------")    

def solveBoard(board):
    if len(board)!= 9 :
        raise Exception("SIZE OF BOARD IS NOT VALID")
    for i in board:
        if len(i) != 9 :
            raise Exception( "SIZE OF BOARD IS NOT VALID")
    
    if not solve(board):
        raise Exception( "CAN NOT SOLVE THE BOARD")

    return board