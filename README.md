# Turn Based Connection Game AI

Using Python, I implemented various connection based games and solutions for the AI to follow.

## Tic Tac Toe 
I used minimax algorithm and reinforced learning for the computer. As it is possible to run through all game states, the worst case scenario for the AI is a draw. 

## Connect Four
I used minimax algorithm. The evaluation board function is the most crucial, as it decides the value of the AI's moves. Since it cannot iterate through all possible games states (~4.5 trillion), it must return the move with most value, given a certain depth. I set the evaluation function to support its own streaks (4 in a row, 3 in a row, 2 in a row), while simultaneously attempting to stop the opponent's streaks. Further improvement is needed.


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

For Connect Four, the game has been solved, so it is possible to employ an unbeatable AI. An improvement would be to use that evaluation instead of the one I'm currently using.

In addition, I want to make the game more user friendly; make it more visual and mouse-click based.
