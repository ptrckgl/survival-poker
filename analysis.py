"""
This file is to analyse hand win percentages against other random hands
How it will work:
1. Get hand amount
2. Using that hand amount, generate set playthroughs (say 1 million) of that hand amount
3. For every hand in each playthrough, get it's identity, so for example,
(pocket aces, 4 6 offsuit, 10 Jack suited)
4. If a single hand wins, add '1' to it's identity value (every identity value starts at 0).
If multiple hands win, then add 1/(hands won altogether) to the hand's identity value, if that
specific hand won. If the hand didn't win, just don't add any value to it.
5. Eventually, after the 1 million playthroughs for example, the hand which won the most will
have the highest value in it's identity value (say, pocket aces might have 300000 out of 1 million)
6. The data will be stored in a 2d list, where the each row/column will be a card value from A to 2
The diagonals will be pocket pairs (the suit doesn't matter because they can never be suited). The
upper triangle will be for suited combinations, and bottom one will be unsuited. For example
    A   K   Q   J   T   9   ...
A   ?   29  24
K       ?
Q           ?
J               ?
T                   ?
9                       ?
In this table, AK suited will have a 29% chance of winning, and AQ suited will have a 24% chance.
7. To determine the percentage of wins, just divide the value of a hand's identity with the total
number of simulations run

DISCLAIMER: These values will be made without caring about what cards are on the flop, turn and
river. For example, if AA is 39% chance of winning with 3 hands in play, this will be over a sample
space of 1 million where every hand was in play for every single simulation, and no hand was folded
during the round. This is kind of a general indication of strength of hands while put against x
other amount of hands, assuming every hand is in play. The more amount of hands which are in play,
the lower percentage of wins each hand will have. If this is made correctly, pocket aces should
have the largest win percentage, and not 7 2 off...
"""

import engine
import main
import random

HANDS = 3
SIMULATIONS = 1000000
INDEXES = {
    'A': 0,
    'K': 1,
    'Q': 2,
    'J': 3,
    'T': 4,
    '9': 5,
    '8': 6,
    '7': 7,
    '6': 8,
    '5': 9,
    '4': 10,
    '3': 11,
    '2': 12
}
CARDS = main.generate_cards()


def main():
    """The main program to analyse hands."""
    identity_list = create_identity_list()

    for sim in range(SIMULATIONS):
        # Generate the hands and board
        cards_used = []
        hands_array = main.generate_hands(cards_used, cards, hand_amount)
        ftr = main.generate_ftr(cards_used, cards)

        # Find strengths of each hand and determine winner list
        strengths = main.get_strengths(hands_array, ftr, hand_amount)
        winner = determine_winner(hands_array, ftr, strengths)

        # Get the 'identities' of every hand



def create_identity_list():
    """Generates and returns the empty (zeroed) 2 dimensional identity list"""
    identity_list = []

    # Note, just doing it like this incase some cards want to be removed from INDEXES dictionary
    # Add the rows (and cols) into the identity array
    for i in range(len(INDEXES)):
        identity_list.append([0 for j in range(len(INDEXES))])

    return identity_list


def get_identities(hands_array):
    """
    Gets the identity 'index' for each hand. The 'index' of each hand is based off the
    identity 2d list. The index starts at the top left (where pocket aces is located), with
    identity value 0. The next index is index 1, which would be AK suited. Once it gets to A2
    suited which will be index 12, it will go down to the next row where index 13 will be
    AK off suit.
    """


if __name__ == '__main__':
    main()
