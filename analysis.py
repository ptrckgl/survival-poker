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

'''
INDEX TABLE
  A   K   Q   J   T   9   8   7   6   5   4   3   2
A 0   1   2   3   4   5   6   7   8   9   10  11  12
K 13  14  15  16  17  18  19  20  21  22  23  24  25
Q 26  27  28  29  30  31  32  33  34  35  36  37  38
J 39  40  41  42  43  44  45  46  47  48  49  50  51
T 52  53  54  55  56  57  58  59  60  61  62  63  64
9 65  66  67  68  69  70  71  72  73  74  75  76  77
8 78  79  80  81  82  83  84  85  86  87  88  89  90
7 91  92  93  94  95  96  97  98  99  100 101 102 103
6 104 105 106 107 108 109 110 111 112 113 114 115 116
5 117 118 119 120 121 122 123 124 125 126 127 128 129
4 130 131 132 133 134 135 136 137 138 139 140 141 142
3 143 144 145 146 147 148 149 150 151 152 153 154 155
2 156 157 158 159 160 161 162 163 164 165 166 167 168
'''

HANDS = 2  # MAX 9 HANDS
SIMULATIONS = 100000
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
    frequency = create_identity_list()

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
            row_col = get_row_col_index(hand_identities[hand])
            if winner[hand] == 1:  # The corresponding hand won
                identity_list[row_col[0]][row_col[1]] += 1.0/winning_hands
            frequency[row_col[0]][row_col[1]] += 1

    # Turn the identity list into percentages using frequency list
    percentage_list = convert_to_percentages(identity_list, frequency)

    # Nicely print the results
    print_results(percentage_list)


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


def convert_to_percentages(identity_list, frequency):
    """Converts hand wins to percentages using the frequency list."""
    percentage_list = create_identity_list()

    for row in range(len(INDEXES)):
        for col in range(len(INDEXES)):
            if frequency[row][col] == 0:
                percentage_list[row][col] = -1
            else:
                percentage_list[row][col] = (identity_list[row][col] / frequency[row][col]) * 100

    return percentage_list


def print_results(identity_list):
    """Prints the results in a nice manner"""
    inversed_indexes = {v: k for k, v in INDEXES.items()}
    highest_val = identity_list[0][0]
    highest_hand = "A A"
    lowest_val = highest_val
    lowest_hand = "A A"
    running_total = 0.0

    print(f"This table contains win percentages from comparing {HANDS} hands")
    print(f"against each other in {SIMULATIONS} simulations\n")
    print("     A     K     Q     J     T     9     8     7     6     5     4     3     2\n")
    for row in range(len(INDEXES)):
        print(f"{inversed_indexes[row]}  ", end="")
        for col in range(len(INDEXES)):
            print(f"{format(identity_list[row][col], '.2f')}", end=" ")  # To two decimal places

            # Update highest/lowest values
            if identity_list[row][col] > highest_val:
                highest_val = identity_list[row][col]
                highest_hand = f"{inversed_indexes[row]} {inversed_indexes[col]}"
                if row != col:
                    suited = True if col > row else False
                    highest_hand += ' suited' if suited else ' off'

            if identity_list[row][col] < lowest_val:
                lowest_val = identity_list[row][col]
                lowest_hand = f"{inversed_indexes[row]} {inversed_indexes[col]}"
                if row != col:
                    suited = True if col > row else False
                    lowest_hand += ' suited' if suited else ' off'

            # Update running total
            running_total += identity_list[row][col]

        print("\n")

    print(f"The hand with the highest win percentage was {highest_hand} ", end="")
    print(f"with {format(highest_val, '.2f')}% of hands won")
    print(f"The hand with the lowest win percentage was {lowest_hand} ", end="")
    print(f"with {format(lowest_val, '.2f')}% of hands won")
    print(f"The average win percentage overall was ", end="")
    print(f"{format(running_total / len(INDEXES) ** 2, '.2f')}%")


if __name__ == '__main__':
    analyse()
