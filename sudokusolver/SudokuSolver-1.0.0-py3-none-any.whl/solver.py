
 #__init__.py   
__version__ = "0.0.1"     

# board = [
#     [7,8,0,4,0,0,1,2,0],
#     [6,0,0,0,7,5,0,0,9],
#     [0,0,0,6,0,1,0,7,8],
#     [0,0,7,0,4,0,2,6,0],
#     [0,0,1,0,5,0,9,3,0],
#     [9,0,4,0,6,0,0,0,5],
#     [0,7,0,3,0,0,0,1,2],
#     [1,2,0,0,0,7,4,0,0],
#     [0,4,9,2,0,6,0,0,7]
# ]

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
                # print("found solution for", i, j)        
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
# print(valid(4, 0, 4, 9, board))   
def printBoard(board):   
    for i in board:
        print(i) 
    print("---------------------------")    
    # solve()
    # for k in board:
    #     print(k)


def solveBoard(board):
    if len(board)!= 9 :
        raise Exception("SIZE OF BOARD IS NOT VALID")
    for i in board:
        if len(i) != 9 :
            raise Exception( "SIZE OF BOARD IS NOT VALID")
    
    if not solve(board):
        raise Exception( "CAN NOT SOLVE THE BOARD")

    return board