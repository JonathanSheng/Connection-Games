# Tic Tac Toe Bot

Using Python, I implemented the game of Tic Tac Toe. You can play with another person or against a bot. For the bot, I implemented two methods of how they would play. For the first one, I used the minimax algorithm, optimized with alpha beta pruning, where the bot would always make the optimal move, thus never losing. For the second, I used reinforcement learning, using value iteration, with two agents and saved the memory of game states to the bot you would play against. You can adjust the difficulty based on the number of rounds the bots train.


### Prerequisites
You'll need numpy and pickle (pickle should be installed in Python2 and Python3 by default).

```
pip install numpy
```

### Installing
Copy and run in Git Bash.
```
$ git clone https://github.com/JSheng1689/Tic-Tac-Toe-AI.git
```
Afterwards, for the reinforced learning agent, uncomment the code denoted at the bottom of the file. Adjust the number of rounds based on how trained you want the bot to be.

### Future Improvements
Implementing a Monte Carlo Search Tree as another unique approach. Games such as Go and Chess benefit from MCST, as they have a massive number of game states.
In addition, I want to make the game more user friendly; for example, clicking the cells instead of declaring the cell as a number
