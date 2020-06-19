import numpy as np
"""
Used Alpha-Beta Pruning to optimize Minimax algorithm.
The algorithm checks the maximizers and minimizers and when it isn't possible to beat a better option,
it stops searching and moves onto the next options.
I evaluate the board by counting the length and number of streaks (i.e. 3 in a row is worth more than 2 in a row).
"""
BOARD_COLS = 7
BOARD_ROWS = 6
AI = 1
PLAYER = -1
DEPTH = 4

#AI is 1, Human is -1
class State:
    """
    Represents the state of the board we're in
    """
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.playerSymbol = AI
    def showBoard(self):
        """
        Objective: Print the board for the user
        """
        for i in range(BOARD_ROWS):
            print('        ------------------------------------')
            row_symbol = '        | '
            for j in range(BOARD_COLS):
                if self.board[i][j] == 1:
                    row_symbol += ('⚫')
                elif self.board[i][j] == -1:
                    row_symbol += ('⚪')
                else:
                    row_symbol += '  '
                row_symbol += ' | '
            print(row_symbol)
        print('        ------------------------------------')
        print('Column:    1    2    3    4    5    6    7')
    def play(self):
        """
        Objective: Play game against Computer
        """
        while not self.isEnd:    
            p1_action = self.p1.bestMove(self.board)
            self.board[p1_action] = self.playerSymbol
            self.playerSymbol *= -1
            result, self.isEnd = checkWinner(self.board)
            self.showBoard()
            if result is not None:
                if result == AI:
                    print('Computer Wins')
                elif result == PLAYER:
                    print('Player Wins!')
                else:
                    print('Draw')
                self.isEnd = True
                return
            p2_action = self.p2.move(self.board, self.playerSymbol)
            self.board[p2_action] = self.playerSymbol
            self.playerSymbol *= -1
            self.showBoard()
            result, self.isEnd = checkWinner(self.board)
            if result is not None:
                if result == AI:
                    print('Computer wins!')
                elif result == PLAYER:
                    print('Player wins!')
                else:
                    print('Draw')
                self.isEnd = True
                return 
class Player:
    """
    Represents us, the human player
    """
    def __init__(self, name):
        """
        Initialize class for human player
        """
        self.name = name
    def move(self, board, playerSymbol):
        """
        Inputs: the state of the board, and whose turn it is
        Returns: coordinates of the cell player moves to
        Objective: Make human move on board. Replaces valid cell with marker
        """
        while True:
            column = int(input('Choose column: '))
            move = valid_move(board, column)
            if move is not None:
                return move
            else:
                print('The column is filled up')
            
def valid_move(board, column):
    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[i][column - 1] == 0:
            return (i, column - 1)
    return None
#Represents the rewards that will influence the bot's decisions

class Computer:
    """
    Represents the computer we will be playing against
    """
    def __init__(self, name):
        """
        Inputs: name
        Objective: Initialize Computer with a name
        """
        self.name = name
    def bestMove(self, board):
        """
        Inputs: state of given board
        Return: tuple representing the cell the computer should move
        Objective: Decides computer's best move, using minimax algo
        """
        best_score = -float('inf')
        #Starts at the bottom of the board and checks up, takes into account gravity
        for i in range(BOARD_COLS):
            for j in range(BOARD_ROWS - 1, 0, -1):
                #Check if spot available
                if board[j][i] == 0:
                    board[j][i] = AI
                    score = minimax(board, DEPTH, True, -float('inf'), float('inf'))
                    board[j][i] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (j, i)
                    break
        board[best_move] = AI
        return best_move

def check_lines(board, x, y, num):
    """
    Checks the number of pieces in a row for the player or bot
    Use it to check 2, 3, and 4 in a row
    Helper function as sliding window to check entire board
    """
    hori = 0
    vert = 0
    diag_sum1 = 0
    diag_sum2 = 0
    for i in range(x, x + num):
        for j in range(y, y + num):
            hori += board[i][j]
        if hori == num:
            return AI
        if hori == -num:
            return PLAYER
        hori = 0
    for i in range(y, y + num):
        for j in range(x, x + num):
            vert += board[j][i]
        if vert == num:
            return AI
        if vert == -num:
            return PLAYER
        vert = 0
    for i in range(num):
        diag_sum1 += board[x + i][y + i]
    if diag_sum1 == num:
        return AI
    if diag_sum1 == -num:
        return PLAYER
    for i in range(num):
        diag_sum2 += board[x + i][num + y - i - 1]
    if diag_sum2 == num:
        return AI
    if diag_sum2 == -num:
        return PLAYER
    return None
def checkWinner(board):
        """
        Input: state of board
        Returns: 1 or -1, depending on if X or O won, respectively
                0 if draw
                None if game is still in progress
        Objective: check the result of the board, see the outcome
        """
        #Does a 4x4 window and scans entire board
        for i in range(BOARD_ROWS - 3):
            for j in range(BOARD_COLS - 3):
                result = check_lines(board, i, j, 4)
                if result == 1:
                    return AI, True
                elif result == -1:
                    return PLAYER, True
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if board[i][j] == 0:
                    draw = False
                    break
            if not draw:
                break
        if draw:
            return 0, True
        return None, False
def evaluate_board(board):
    """
    There's many ways to evaluate the board.
    I essentially value the streaks and its length.
    4 is good/bad depending on who wins,
    3 is valued 100
    2 is valued 1

    Others ways to evaluate board
    """
    result, _ = checkWinner(board)
    if result == PLAYER:
        return -100000
    else:
        fours = 0
        threes = 0
        twos = 0
        #Check how many fours in a row
        for i in range(BOARD_ROWS - 3):
            for j in range(BOARD_COLS - 3):
                result = check_lines(board, i, j, 4)
                if result == AI:
                    fours += 1
        #Check how many three in a row
        for i in range(BOARD_ROWS - 2):
            for j in range(BOARD_COLS - 2):
                result = check_lines(board, i, j, 3)
                if result == AI:
                    threes += 1
        #Check how many two in a row
        for i in range(BOARD_ROWS - 1):
            for j in range(BOARD_COLS - 1):
                result = check_lines(board, i, j, 2)
                if result == AI:
                    twos += 1
        return (100000*fours + 100*threes + twos)

def minimax(board, depth, isMaximizing, alpha, beta):
    """
    Inputs: state of board, 
            depth indicating level of tree, 
            isMaximizing to denote if minimizing or maximizing player, 
            alpha represents the minimum score that the maximizing player is guaranteed 
            beta represents the maximum score that the minimizing player is guaranteed
    Returns: best score from after running minimax on the given board
    Objective: Runs minimax with alpha beta pruning to check best move for computer

    """
    current_result, _ = checkWinner(board)
    if depth == 0 or current_result is not None: #If game done, return score
        return evaluate_board(board)
    if isMaximizing: #Finds best move if AI is next, maximize score
        best_score = -float('inf')
        for i in range(BOARD_COLS):
            for j in range(BOARD_ROWS - 1, 0, -1):
                #Check if spot available
                if board[j][i] == 0:
                    board[j][i] = AI
                    score = minimax(board, depth-1, False, alpha, beta)
                    board[j][i] = 0
                    best_score = max(score - depth , best_score) #We want the AI to win ASAP
                    alpha = max(alpha, best_score) #Maximize score, best explored option for maximizer from the current state
                    if alpha >= beta: #A better option exists so prune 
                        return best_score
                    break
        return best_score
    else:
        best_score = float('inf')
        for i in range(BOARD_COLS):
            for j in range(BOARD_ROWS - 1, 0, -1):
                #Check if spot available
                if board[j][i] == 0:
                    board[j][i] = PLAYER
                    score = minimax(board, depth-1, True, alpha, beta)
                    board[j][i] = 0
                    best_score = min(depth + score, best_score) #We want the AI to lose as slowly as possible
                    beta = min(beta, best_score) #Minimize score, best explored option for minimizer from the current state
                    if beta <= alpha:
                        return best_score
                    break
        return best_score



print('Computer goes first :P ')
p1 = Computer('p1')
p2 = Player('p2')
st = State(p1, p2)
# board = [[0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0],
#          [0,-1,0,0,0,0,0],
#          [0,1,0,-1,0,0,0],
#          [0,1,1,1,0,0,0],
#          [0,1,1,-1,0,0,0]]
# print(checkWinner(board))
st.showBoard()

st.play()