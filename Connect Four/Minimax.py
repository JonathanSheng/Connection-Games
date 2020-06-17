import numpy as np
"""
Used Alpha-Beta Pruning to optimize Minimax algorithm.
The algorithm checks the maximizers and minimizers and when it isn't possible to beat a better option,
it stops searching and moves onto the next options.
"""
BOARD_COLS = 7
BOARD_ROWS = 6
AI = 1
PLAYER = -1

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
            print('----------------------')
            row_symbol = '| '
            for j in range(BOARD_COLS):
                if self.board[i][j] == 1:
                    row_symbol += ('⚫')
                elif self.board[i][j] == -1:
                    row_symbol += ('⚪')
                else:
                    row_symbol += ''
                row_symbol += ' | '
            print(row_symbol)
        print('----------------------')
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
                    print('You have defied logic!')
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
        for i in range(BOARD_ROWS - 1, 0, -1):
            if board[i][j] == 0:
                return (i, j)
        return None
#Represents the rewards that will influence the bot's decisions
scores = { 
    -1: -10,
    1: 10,
    0: 0
}
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
                    score = minimax(board, 0, False, -float('inf'), float('inf'))
                    board[j][i] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (j, i)
                    break
        board[best_move] = AI
        return best_move

def check_four(board, x, y):
    hori = 0
    vert = 0
    for i in range(x, x + 4):
        for j in range(y, y + 4):
            hori += board[i][j]
        if hori == 4:
            return AI
        if hori == -4:
            return PLAYER
    for i in range(y, y + 4):
        for j in range(x, x + 4):
            vert += board[j][i]
        if vert == 4:
            return AI
        if vert == -4:
            return PLAYER
          
            
    diag_sum1 = sum([board[i][i] for i in range(x, x+4)])
    diag_sum2 = sum([board[i][4 - i - 1] for i in range(x, x + 4)])
    check_diag = max(abs(diag_sum1), abs(diag_sum2))
    if check_diag == 4:
        if diag_sum1 == 4 or diag_sum2 == 4:
            return AI
        else:
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
                result = check_four(board, i, j)
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
    if current_result is not None: #If game done, return score
        return scores[current_result]
    if isMaximizing: #Finds best move if AI is next, maximize score
        best_score = -float('inf')
        for i in range(BOARD_COLS):
            for j in range(BOARD_ROWS - 1, 0, -1):
                #Check if spot available
                if board[j][i] == 0:
                    board[j][i] = AI
                    score = minimax(board, depth+1, False, alpha, beta)
                    board[j][i] = 0
                    best_score = max(score - depth , best_score) #We want the AI to win ASAP
                    alpha = max(alpha, best_score) #Maximize score, best explored option for maximizer from the current state
                    if beta <= alpha: #A better option exists so prune 
                        return best_score
        return best_score
    else:
        best_score = float('inf')
        for i in range(BOARD_COLS):
            for j in range(BOARD_ROWS - 1, 0, -1):
                #Check if spot available
                if board[j][i] == 0:
                    board[j][i] = PLAYER
                    score = minimax(board, depth+1, True, alpha, beta)
                    board[j][i] = 0
                    best_score = min(depth + score, best_score) #We want the AI to lose as slowly as possible
                    beta = min(beta, best_score) #Minimize score, best explored option for minimizer from the current state
                    if beta <= alpha:
                        return best_score
        return best_score


# print('Please follow this cell notation for movemaking: ')
# print_board(state)
# print('Computer goes first :P ')
# p1 = Computer('p1')
# p2 = Player('p2')

# st = State(p1, p2)
# print(st.board)
# st.play()
