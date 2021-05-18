# Survival Poker

To all Poker fans! This is a fun little game where essentially you try and pick which hand you think is going to win!

## Main characteristics
- You choose how many hands you want at the table (Between 2 and 9).
- You begin with 5 lives and 0 score.
- You are shown each hand prior to seeing the Flop, Turn and River.
- You choose which hand you think is going to win the round by entering the number of that hand.
- Let Pseudorandomness determine your fate!
- Choosing the winning hand will result in gaining 1 score.
- Choosing a hand which is part of a split pot will result in no change.
- Choosing a losing hand will result in losing 1 life.
- The game ends when you lose all your lives!


## Extra Information
- The program is run by typing 'Python3 main.py' in the command line.
- There is a tests.py file which contains tests to ensure complete coverage of main.py and engine.py.
- There is an analysis.py file which essentially calculates overall win percentages of certain hands, where the user determines a certain number of hands in play and the amount of times the simulation is run. Pocket Aces should always have the higest win percentage!
- You cannot change the number of hands in play during execution of main.py.
- As far as I know, there are no errors in comparing the winner (or even a split pot) between two different hands, even in extreme edge cases.
- My highest score when playing 3 handed is 14! ( not 14 factorial :') )
