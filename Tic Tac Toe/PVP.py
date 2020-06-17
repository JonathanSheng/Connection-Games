import numpy as np
BOARD_COLS = BOARD_ROWS = 3
state = [['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']]
#X is 1, O is -1
class State:
    """
    Represents the state of the board we are in
    """
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.playerSymbol = 1
    def checkWinner(self):
        """
        Returns 1 or -1, depending on if X or O won, respectively
        Returns 0 if draw
        Returns None if game is still in progress
        """
        vert = 0
        hori = 0
        draw = True
        #Horizontal, Vertical, or Draw check
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                vert += self.board[j][i]
                hori += self.board[i][j]
                if self.board[i][j] == 0:
                    draw = False
            if vert == 3 or hori == 3:
                self.isEnd = True
                return 1
            if vert == -3 or hori == -3:
                self.isEnd = True
                return -1
            vert = hori = 0
        #Two diagonals to check
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
        check_diag = max(abs(diag_sum1), abs(diag_sum2))
        if check_diag == 3:
            if diag_sum1 == 3 or diag_sum2 == 3:
                self.isEnd = True
                return 1        
            else:
                self.isEnd = True
                return -1
        if draw:
            self.isEnd = True
            return 0
        self.isEnd = False
        return None
    def showBoard(self):
        """
        Print the board for the user
        """
        for i in range(BOARD_ROWS):
            print('-------------')
            row_symbol = '| '
            for j in range(BOARD_COLS):
                if self.board[i][j] == 1:
                    row_symbol += ('X')
                elif self.board[i][j] == -1:
                    row_symbol += ('O')
                else:
                    row_symbol += ''
                row_symbol += ' | '
            print(row_symbol)
        print('-------------')
    def play(self):
        while not self.isEnd:
            p1_action = self.p1.move(self.board, self.playerSymbol)
            self.board[p1_action] = self.playerSymbol
            self.playerSymbol *= -1
            result = self.checkWinner()
            self.showBoard()
            if result is not None:
                if result == 1:
                    print(self.p1.name, 'Wins')
                elif result == -1:
                    print(self.p2.name, 'Wins')
                else:
                    print('Draw')
                self.isEnd = True
                return
            p2_action = self.p2.move(self.board, self.playerSymbol)
            self.board[p2_action] = self.playerSymbol
            self.playerSymbol *= -1
            self.showBoard()
            result = self.checkWinner()
            if result is not None:
                if result == 1:
                    print(self.p1.name, 'wins!')
                elif result == -1:
                    print(self.p2.name, 'wins!')
                else:
                    print('Draw')
                self.isEnd = True
                return     
class Player:
    """
    Class used for us to make two players to play against
    """
    def __init__(self, name):
        self.name = name
    def move(self, board, playerSymbol):
        while True:
            cell = int(input('Choose cell: '))
            i = (cell-1) // 3
            j = (cell-1)%3
            if board[i][j]== 0:
                board[i][j] == playerSymbol
                return (i, j)
            else:
                print('Invalid Move')
def print_board(game_state):
    print('-------------')
    print('| ' + str(game_state[0][0]) + ' | ' + str(game_state[0][1]) + ' | ' + str(game_state[0][2]) + ' |')
    print('-------------')
    print('| ' + str(game_state[1][0]) + ' | ' + str(game_state[1][1]) + ' | ' + str(game_state[1][2]) + ' |')
    print('-------------')
    print('| ' + str(game_state[2][0]) + ' | ' + str(game_state[2][1]) + ' | ' + str(game_state[2][2]) + ' |')
    print('-------------')
print('Please follow this cell notation for movemaking: ')
print_board(state)
p1 = Player('p1')
p2 = Player('p2')
st = State(p1, p2)
st.play()