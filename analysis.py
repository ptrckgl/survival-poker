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
SIMULATIONS = 10000
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


def analyse():
    """The main program to analyse hands (not named main because it's imported)."""
    identity_list = create_identity_list()

    for sim in range(SIMULATIONS):
        # Generate the hands and board
        cards_used = []
        hands_array = main.generate_hands(cards_used, CARDS, HANDS)
        ftr = main.generate_ftr(cards_used, CARDS)

        # Find strengths of each hand and determine winner list, and amount of winning hands
        strengths = main.get_strengths(hands_array, ftr, HANDS)
        winner = main.determine_winner(hands_array, ftr, strengths)
        winning_hands = len(main.get_winning_hands(winner))

        # Get the 'identities' of every hand
        hand_identities = get_identities(hands_array)

        # Add 1 to corresponding identity value if the hand won
        for hand in range(HANDS):
            if winner[hand] == 1:  # The corresponding hand won
                row_col = get_row_col_index(hand_identities[hand])
                identity_list[row_col[0]][row_col[1]] += 1.0/winning_hands

    # TODO: Turn the identity list into percentages out of total simulations run

    # Nicely print the results
    print_results(identity_list)


def create_identity_list():
    """Generates and returns the empty (zeroed) 2 dimensional identity list"""
    identity_list = []

    # Note, just doing it like this incase some cards want to be removed from INDEXES dictionary
    # Add the rows (and cols) into the identity array
    for i in range(len(INDEXES)):
        identity_list.append([0.0 for j in range(len(INDEXES))])

    return identity_list


def get_identities(hands_array):
    """
    Gets the identity 'index' for each hand. The 'index' of each hand is based off the
    identity 2d list. The index starts at the top left (where pocket aces is located), with
    identity value 0. The next index is index 1, which would be AK suited. Once it gets to A2
    suited which will be index 12, it will go down to the next row where index 13 will be
    AK off suit.
    """
    identity_list = []

    for i in range(HANDS):
        # First - check if the hand is suited
        suited = True if hands_array[(i * 4) + 1] == hands_array[(i * 4) + 3] else False

        # Next, extract face values from the hand and get their index
        value1 = hands_array[(i * 4)]
        value2 = hands_array[(i * 4) + 2]
        index1 = INDEXES[str(value1)]
        index2 = INDEXES[str(value2)]

        if suited:  # We want to go into the upper triangle of the 2d list
            if index1 < index2:  # index1 is a higher face value
                overall_index = index1 * len(INDEXES) + index2
            else:  # index1 can never be equal to index2 if suited hand
                overall_index = index2 * len(INDEXES) + index1
        else:  # We want to go into the lower triangle of the 2d list
            if index1 > index2:  # index1 is the lower face value
                overall_index = index1 * len(INDEXES) + index2
            else:
                overall_index = index2 * len(INDEXES) + index1

        identity_list.append(overall_index)

    return identity_list


def get_row_col_index(index):
    """Based off the total index of the hand, get it's corresponding row and column."""
    row_col = [0, 0]
    while index >= len(INDEXES):
        index -= len(INDEXES)
        row_col[0] += 1
    row_col[1] = index

    return row_col


def print_results(identity_list):
    """Prints the results in a nice manner"""
    for row in identity_list:
        print(row)


if __name__ == '__main__':
    analyse()
