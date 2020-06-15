

def solver(board):
    find = is_emp(board)

    if not find:
        return board
    else:
        row, col = find
    for i in range(1,10):
        if is_valid(board, i,find):
            board[row][col]=i

            if solver(board):
                return board

            board[row][col] = 0
    return False


def print_board(board):
    for i in range(len(board)):
        if i%3==0:
            print("------------------------")
        for j in range(len(board[0])):
            if j%3==0:
                print("|",end =" ")
            if j==8:
                print(board[i][j], end="|\n")
            else:
                print(board[i][j], end = " ")


def is_emp(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j)
    return False


def is_valid(board, num, pos):
    check= set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            yo = board[i][j]
            check.add(str(yo) + "row" + str(i))
            check.add(str(yo) + "column" + str(j))
            check.add(str(yo) + "box" + str(i // 3) + "-" + str(j // 3))
    c1 = str(num) + "row" + str(pos[0]) in check
    c2 = str(num) + "column" + str(pos[1]) in check
    c3 = str(num) + "box" + str(pos[0] // 3) + "-" + str(pos[1] // 3) in check
    if c1 or c2 or c3:
        return False
    else:
        return True




