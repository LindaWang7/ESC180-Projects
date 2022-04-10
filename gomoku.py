"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "w" or board[i][j] == "b":
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):

    y_start= (y_end) - (d_y*(length-1))
    x_start= (x_end) - (d_x*(length-1))

    blocked=0
    l=len(board)-1
    if (y_start - d_y)<0 or (x_start - d_x) <0 or (y_start - d_y)>l or (x_start - d_x)>l or \
            (board[y_end][x_end]!=board[y_start - d_y][x_start - d_x] and board[y_start - d_y][x_start - d_x]!= " "):
        blocked += 1

    if (y_end + d_y)<0 or (x_end + d_x) <0 or (y_end + d_y)>l or (x_end + d_x)>l or \
            (board[y_end][x_end]!=board[y_end + d_y][x_end + d_x] and board[y_end + d_y][x_end + d_x]!= " "):
        blocked+=1

    if blocked==2:
        return "CLOSED"
    elif blocked ==1:
        return "SEMIOPEN"
    else:
        return "OPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    liststore = []
    keepgoing = True
    xpos = x_start
    ypos = y_start

    keepgoing = True
    while keepgoing:
        load = True
        top = True
        bottom = True
        if (xpos + d_x*(length - 1)  == 7 and d_x == 1) or (xpos + d_x*(length - 1) == 0 and d_x == -1) or (ypos + d_y*(length - 1) == 7 and d_y == 1):
            keepgoing = False
        for i in range (length):
            if board[ypos + i*d_y][xpos + i*d_x] != col:
                load = False

        notin = True
        #top left
        if xpos == 0 and ypos == 0 and (d_x == 1 or d_x == 0):
            notin = False
            top = False
            if board[ypos + d_y*(length - 1)+d_y][xpos + d_x*(length - 1)+d_x] == col:
                load = False
        #right (end right or straght)
        if xpos + length - 1 == 7 and d_x == 1:
            notin = False
            bottom = False
            if ypos == 0 and d_y != 0:
                top = False
            elif board[ypos-d_y][xpos-d_x] == col:
                load = False
        #down (start to right )
        if ypos == 0 and d_y == 1 and d_x == 1:
            notin = False
            top = False
            if xpos + d_x*(length - 1) == 7:
                bottom = False
            elif board[ypos + d_y*(length - 1) + d_y][xpos + d_x*(length - 1) + d_x] == col:
                load = False
        #down (top to bottom)
        if ypos == 0 and d_y == 1 and d_x == 0:
            notin = False
            top = False
            if board[ypos + d_y*(length - 1) + d_y][xpos + d_x*(length - 1) + d_x] == col:
                load = False
        #down top to Left
        if ypos == 0 and d_y == 1 and d_x == -1:
            notin = False
            top = False
            if xpos + d_x*(length - 1) == 0:
                bottom = False
            elif board[ypos + d_y*(length - 1) + d_y][xpos + d_x*(length - 1) + d_x] == col:
                load = False
        #right straght or down (start)
        if xpos == 0 and d_x == 1 :
            notin = False
            top = False
            if ypos + d_y*(length - 1) == 7 and d_y != 0:
                bottom = False
            elif board[ypos + d_y*(length - 1) + d_y ][xpos + d_x*(length - 1) + d_x] == col:
                load = False
        #down end Left or Right
        if ypos + length - 1 == 7 and d_y == 1 and d_x != 0:
            notin = False
            bottom = False
            if xpos == 0 or xpos == 7:
                top = False
            elif board[ypos - d_y][xpos - d_x] == col:
                load = False
        #down end straght
        if ypos + length - 1 == 7 and d_y == 1 and d_x == 0:
            notin = False
            bottom = False
            if board[ypos - d_y][xpos - d_x] == col:
                load = False
        #down (start) to left
        if xpos == 7 and d_y == 1 and d_x == -1:
            notin = False
            top = False
            if ypos + d_y*(length-1) == 7:
                bottom = False
            elif board[ypos + d_y * (length - 1) + d_y][xpos + d_x * (length - 1) + d_x] == col:
                load = False

        if notin == True and ((board[ypos - d_y][xpos - d_x] == col) or (board[ypos + d_y*(length - 1) + d_y ][xpos + d_x*(length - 1) + d_x] == col)) :
            load = False

        if top == False and bottom == False:
            load = False

        if load == True:
            liststore.append([xpos + (length-1)*d_x, ypos + (length-1)*d_y])

        xpos += d_x
        ypos += d_y

    open_seq_count = 0
    semi_open_seq_count = 0
    for i  in range (len(liststore)):
        x_end = liststore[i][0]
        y_end = liststore[i][1]
        word = is_bounded(board, y_end, x_end, length, d_y, d_x)
        if word == "OPEN":
            open_seq_count += 1
        elif word == "SEMIOPEN":
            semi_open_seq_count += 1
    return open_seq_count, semi_open_seq_count


def detect_rows(board, col, length):
    # uses for loops to check different directions of a row
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range(len(board)):
        # col
        a = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += a[0]
        semi_open_seq_count += a[1]

    for i in range(len(board)):
        # row
        a = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += a[0]
        semi_open_seq_count += a[1]

    # left
    for i in range(length, len(board)):
        a = detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += a[0]
        semi_open_seq_count += a[1]

    for i in range(1, len(board) - length + 1):
        a = detect_row(board, col, i, 7, length, 1, -1)
        open_seq_count += a[0]
        semi_open_seq_count += a[1]

    # right
    for i in range(len(board) - length + 1):
        a = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += a[0]
        semi_open_seq_count += a[1]

    for i in range(1, len(board) - length + 1):
        a = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += a[0]
        semi_open_seq_count += a[1]

    return open_seq_count, semi_open_seq_count


def search_max(board):
    # make a 2D list that stores all the scores of each position
    tempboard = board
    boardlist = []
    move_y, move_x = 0, 0
    maxscore = -10000000
    for i in range(len(board)):
        alist = []
        for j in range(len(board)):
            alist.append(-1000000)
        boardlist.append(alist)

    # for loop to load the scores for each pos into tempboard
    for x in range(len(board)):
        for y in range(len(board)):
            if tempboard[x][y] == " ":
                tempboard[x][y] = "b"
                a = score(board)
                tempboard[x][y] = " "
                boardlist[x][y] = a
            if tempboard[x][y] == "b" or tempboard[x][y] == "w":
                boardlist[x][y] = - 10000000

    # check for the highest score inside tempboard
    for i in range(len(board)):
        for j in range(len(board)):
            if boardlist[i][j] > maxscore:
                maxscore = boardlist[i][j]
                # might be wrong
                move_y = i
                move_x = j

    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    white = False
    black = False
    draw = True

    # white
    # row
    for k in range(len(board)):
        for i in range(len(board) - 4):
            if board[k][i] == "w" and board[k][i + 1] == "w" and board[k][i + 2] == "w" and board[k][i + 3] == "w" and \
                    board[k][i + 4] == "w":
                white = True
    # col
    for k in range(len(board)):
        for i in range(len(board) - 4):
            if board[i][k] == "w" and board[i + 1][k] == "w" and board[i + 2][k] == "w" and board[i + 3][k] == "w" and \
                    board[i + 4][k] == "w":
                white = True
    # right
    for k in range(4):
        for i in range(4):
            if board[i][k] == "w" and board[i + 1][k + 1] == "w" and board[i + 2][k + 2] == "w" and board[i + 3][k + 3] == "w" and board[i + 4][k + 4] == "w":
                white = True
    # left
    for k in range(4):
        for i in range(len(board) - 1, 3, -1):
            if board[i][k] == "w" and board[i - 1][k + 1] == "w" and board[i - 2][k + 2] == "w" and board[i - 4][k + 4] == "w" and board[i - 3][k + 3] == "w":
                white = True

    # black
    for k in range(len(board)):
        for i in range(len(board) - 4):
            if board[k][i] == "b" and board[k][i + 1] == "b" and board[k][i + 2] == "b" and board[k][i + 3] == "b" and \
                    board[k][i + 4] == "b":
                black = True
    # col
    for k in range(len(board)):
        for i in range(len(board) - 4):
            if board[i][k] == "b" and board[i + 1][k] == "b" and board[i + 2][k] == "b" and board[i + 3][k] == "b" and \
                    board[i + 4][k] == "b":
                black = True
    # right
    for k in range(4):
        for i in range(4):
            if board[i][k] == "b" and board[i + 1][k + 1] == "b" and board[i + 2][k + 2] == "b" and board[i + 3][k + 3] == "b" and board[i + 4][k + 4] == "b":
                black = True
    # left
    for k in range(4):
        for i in range(len(board) - 1, 3, -1):
            if board[i][k] == "b" and board[i - 1][k + 1] == "b" and board[i - 2][k + 2] == "b" and board[i - 4][k + 4] == "b" and board[i - 3][k + 3] == "b":
                black = True

    # draw
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                draw = False

    if white:
        return "White won"
    if black:
        return "Black won"
    if draw:
        return "Draw"
    if draw == False and black == False and white == False:
        return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    play_gomoku(8)
