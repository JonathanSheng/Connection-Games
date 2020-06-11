import numpy as np 
import pickle 
BOARD_COLS, BOARD_ROWS =  3,3

class State:
    """
    Represents the state of the board we are in
    """
    def __init__(self, p1, p2):
        """
        Inputs: p1, p2 both objects of either HumanPlayer or Agent
        Initializes a game state given 2 agents
        Sets an empty board, both players, game in progress, no game state, and gives first symbol as 1, like an X.
        """
        #3x3 array of zeroes
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.p1 = p1
        self.p2 = p2 
        self.isEnd = False
        self.boardHash = None #Represents unique game state pattern
        #Player 1 is 1 and Player 2 is -1
        self.playerSymbol = 1
    def getHash(self):
        """
        Returns the unique game state as a hashable format 
        """
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS)) #Put unique game state in a hashable format
        return self.boardHash
    def available_positions(self):
        """
        Returns a list of possible positions at the current board state
        """
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i][j] == 0:
                    positions.append((i,j))
        return positions
    def update_state(self, position):
        """
        Input: position, tuple of coordinates pointing to a cell on the board
        Objective: Given position, we set that cell on the board to the current player symbol, and toggle symbol.
        """
        self.board[position] = self.playerSymbol
        self.playerSymbol *= -1
    def check_winner(self):
        """
        Objective: Checks the game state's status, if win/draw/ or in progress.
        Returns -1, 0, 1, None based on which player wins, if draw, or in progress, respectively
        """
        #Vertical
        vert = 0
        hori = 0
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                vert += self.board[j][i]
                hori += self.board[i][j]
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
        #No more positions, draw
        if len(self.available_positions()) == 0:
            self.isEnd = True
            return 0
        #Game still in progress, return no reward
        self.isEnd = False
        return None
    def give_reward(self):
        """
        Check winner and depending on which wins, give a reward to that player.
        If draw, you can decide aggressiveness on computer based on the amount you give them.
        """
        result = self.check_winner()
        if result == 1:
            self.p1.feed_reward(1)
            self.p2.feed_reward(0)
        elif result == -1:
            self.p1.feed_reward(0)
            self.p2.feed_reward(1)
        else:
            self.p1.feed_reward(0.1)
            self.p2.feed_reward(0.5)
    def reset(self):
        """
        Objective: Reset the game.
        """
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1   
    def play(self, rounds=100):
        """
        Input: rounds represents the number of games the two computers will play 
        Objective: Simulate matches between the two computers 
        """
        for i in range(rounds):
            if i % 1000 == 0: 
                print('Rounds', i)
            while not self.isEnd:
                positions = self.available_positions()
                p1_action = self.p1.choose_action(positions, self.board, self.playerSymbol) #P1 decides action
                self.update_state(p1_action) #Update board on where p1 decided to move
                board_hash = self.getHash() #Format the current state right now
                self.p1.addState(board_hash) #Add the current board to p1

                win = self.check_winner()
                if win is not None: 
                    #If outcome, give appropriate rewards and reset everything
                    self.give_reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    #Same thing, but player 2 turn
                    positions = self.available_positions()
                    p2_action = self.p2.choose_action(positions, self.board, self.playerSymbol)
                    self.update_state(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.check_winner()
                    if win is not None:
                        self.give_reward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break
        p1.savePolicy() #Remember the data
    def human_play(self):
        """
        Objective: Play against the trained bot
        """
        while not self.isEnd:
            # Player 1
            positions = self.available_positions()
            p1_action = self.p1.choose_action(positions, self.board, self.playerSymbol)
            # take action and upate board state
            self.update_state(p1_action)
            self.showBoard()
            # check board status if it is end
            win = self.check_winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.available_positions()
                p2_action = self.p2.choose_action(positions)

                self.update_state(p2_action)
                self.showBoard()
                win = self.check_winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break
    def showBoard(self):
        """
        Objective: Show the board for user, X are 1, O are -1
        """
        for i in range(0, BOARD_ROWS):
            print('-------------')
            row = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'X'
                if self.board[i, j] == -1:
                    token = 'O'
                if self.board[i, j] == 0:
                    token = ' '
                row += token + ' | '
            print(row)
        print('-------------')

class Agent:
    """
    We're going to be using Epsilon-Greedy Action Selection.
    The higher Epsilon is, the more randomness the machine will explore
    Else, it will exploit the given knowledge of what it knows based on the state value estimations.
    """
    def __init__(self, name, epsilon = .3):
        """
        Initialize a computer agent:
        Sets a name, positions played, the variables needed for reward formula, and state value mapping.
        """
        self.name = name
        self.states = [] #Store positions played
        self.lr = .2
        self.epsilon = epsilon #Set higher if you want more exploration
        self.decay_gamma = .9
        self.states_value = {} #Mapping state to value

    def getHash(self, board):
        """
        Format current board state into hashmap friendly
        """
        boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash

    def choose_action(self, positions, current_board, symbol):
        """
        Input: possible positions, the current state, and who's turn it is.
        Returns: The action/move the agent decides to take based on exploration/exploitation.
        Action is a tuple pointing at which index to move to.
        """
        if np.random.uniform(0, 1) <= self.epsilon:
            #Explore, we choose a random possible position in available positions
            index = np.random.choice(len(positions))
            action = positions[index]
        else: 
            #Exploit, we take action based on highest chance of winning given the info we have
            value_max = -float('inf')
            for p in positions:
                #We run through all positions, based on if we met it before, we assign set a value
                #We want the max value, as it means highest chance of winning, and its respective next move
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                if self.states_value.get(next_boardHash) is None:
                    value = 0
                else:
                    value = self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action = p
        return action

    def addState(self, state):
        """
        Input: the state of the board right now, i.e. where X's and O's are
        We add the state into the agent's history of all game states
        """
        self.states.append(state)

    def feed_reward(self, reward):
        """
        Input: Reward, integer showing how much value to give to the agent
        Use value iteration formula to distribute rewards appropriately
        """
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma*reward - self.states_value[st])
            reward = self.states_value[st]

    def savePolicy(self):
        """
        This is how the Agent will remember the data of past games.
        We are loading our hashmap of game states and their values into a pickle file.
        """
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        """
        This is how we upload the information to the Agent from a past training iteration.
        """
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

    def reset(self):
        """
        Reset the memory of boards played up to the current board.
        """
        self.states = []

class HumanPlayer:
    """
    This will be the class used for us, humans, to play against the bot.
    """
    def __init__(self, name):
        self.name = name
    def choose_action(self, positions):
        while True:
            cell = int(input('Please input the number correlating to the cell: '))
            move = (((cell-1) // 3),((cell-1)%3))
            if move in positions:
                return move
            else:
                print('Invalid Cell, please try again')
    def addState(self, state):
        pass
    def feedReward(self, reward):
        pass
    def reset(self):
        pass


def print_board(game_state):
    """
    Helper function to print out how I want to denote the cell we point to.
    """
    print('----------------')
    print('| ' + str(game_state[0][0]) + ' | ' + str(game_state[0][1]) + ' | ' + str(game_state[0][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[1][0]) + ' | ' + str(game_state[1][1]) + ' | ' + str(game_state[1][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[2][0]) + ' | ' + str(game_state[2][1]) + ' | ' + str(game_state[2][2]) + ' |')
    print('----------------')

#Uncomment below to run two AI against each other, increase rounds to improve their performance
# p1 = Agent("p1")
# p2 = Agent("p2")
# st = State(p1, p2)
# print("training...")
# st.play(20000)

# Human vs AI
p1 = Agent("computer", epsilon=0)
p1.loadPolicy("policy_p1") #Load the data/memory to new agent

p2 = HumanPlayer("human")

st = State(p1, p2)
state = [['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']]
print('Please input the move based on the number correlating to the desired cell')
print_board(state)
st.human_play()
