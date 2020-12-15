import sys


class Unbuffered(object):
    """time.sleep() code"""

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)


# Global Variables
HAND1_WIN = 1
HAND2_WIN = 2
SPLIT_POT = 4


def pairs(hand, ftr):
    """Determine the strength value of a hand by checking pair combinations."""

    strength = 1  # Minimum strength - high card
    common = [1, 1]  # Max pairs on board is 2
    card_common = []

    # Get info about amount of unique_pairs on board, and what card values those pairs are
    unique_pairs = find_pairs_on_board(ftr, common, card_common)

    if hand[0] == hand[2]:  # Pocket Paired Hand
        pocket_pair = 2  # 2 cards of same value so far

        # Here - find any common cards with hand and the board
        x = 0
        while x <= 8:
            if hand[0] == ftr[x]:  # hand[0] == hand[2] so only need to check one
                pocket_pair += 1
            x += 2

        strength = get_strength_pocket_pair(common, unique_pairs, pocket_pair)

    else:  # Non Pocket Paired Hand
        common_cards_1 = 1  # For first card in hand
        common_cards_2 = 1  # For second card in hand

        # Here - find any common cards with hand and the board
        x = 0
        while x <= 8:
            if hand[0] == ftr[x]:
                common_cards_1 += 1
            elif hand[2] == ftr[x]:
                common_cards_2 += 1
            x += 2

        strength = get_strength_not_pocket_pair(hand, common, card_common, unique_pairs,
                                                common_cards_1, common_cards_2)

    return strength


def find_pairs_on_board(ftr, common, card_common):
    """Find pairs on the board and return the amount of unique pairs."""

    used_ftr = []
    unique_pairs = 0
    found_pair = False
    count = 0

    while count < 4:  # Loop for finding pairs on the board
        loop = True
        x = len(used_ftr)
        # First - using the used_ftr array, check if the specific card value ftr[count * 2]
        # has already been scanned for previously in the array
        while x > 0:
            if used_ftr[x - 1] == ftr[count * 2]:
                loop = False  # ftr[count * 2] has already been 'scanned for', or dealt with
                break
            x -= 1

        if loop:  # The card being scanned for, ftr[count * 2], hasn't been scanned for before
            i = count * 2 + 2
            while i <= 8:  # '8' representing the max face_value index in ftr array (5 cards)
                if ftr[count * 2] == ftr[i]:
                    common[unique_pairs] += 1
                    common_index = i  # Want to know what index the card value is found at
                    found_pair = True
                i += 2
            used_ftr.append(ftr[count * 2])
        count += 1

        if found_pair:  # There was a unique pair of cards found
            card_common.append(ftr[common_index])
            unique_pairs += 1  # When this gets to two, will never go higher
            found_pair = False

    return unique_pairs


def get_strength_pocket_pair(common, unique_pairs, pocket_pair):
    """Find and return the strength of a hand if the hand itself is a pocket pair."""

    if pocket_pair == 2:  # No common cards on the board with the hand - pair at worst
        if unique_pairs == 1:
            if common[0] == 3:
                strength = 7  # Full House
            elif common[0] == 4:
                strength = 8  # 4 OAK
            else:
                strength = 3  # Two Pair
        elif unique_pairs == 2:
            if common[0] == 3 or common[1] == 3:
                strength = 7  # Full House
            elif common[0] == 4 or common[1] == 4:
                strength = 8  # 4 OAK
            else:
                strength = 3  # Two Pair
        else:  # The only pair on board is the hand itself
            strength = 2
    elif pocket_pair == 3:  # One common card on the board with hand - 3OAK at worst
        if unique_pairs == 1:
            if common[0] == 4:
                strength = 8  # 4OAK
            else:
                strength = 7  # Full House
        elif unique_pairs == 2:
            strength = 7  # Full House - the strength cannot possibly be a 4OAK
        else:
            strength = 4  # 3OAK
    elif pocket_pair == 4:
        strength = 8  # 4OAK - two common cards on board with hand

    return strength


def get_strength_not_pocket_pair(hand, common, card_common, unique_pairs, common_cards_1,
                                 common_cards_2):
    """Find and return the strength of a non-pocketed pair."""

    if common_cards_1 >= 2 and common_cards_2 >= 2:
        # At least a two pair - using both cards in hand
        strength = 3  # Two Pair at worst
        if unique_pairs == 1:
            # Impossible for there to be a quads or unique_pairs == 2 in this situation
            if common[0] == 3:
                strength = 7  # Full House

        if common_cards_1 >= 3 or common_cards_2 >= 3:
            strength = 7  # Full House
            if common_cards_1 == 4 or common_cards_2 == 4:
                strength = 8  # 4OAK

    elif common_cards_1 >= 2:  # There is at least 1 common card on the board with hand[0]
        strength = 2  # At least a pair
        if unique_pairs == 1:
            if card_common[0] == hand[0]:  # The pair on the board is same value as hand[0]
                strength = 4  # 3OAK
            else:
                strength = 3  # Two Pair At Least
                if common[0] == 3:
                    strength = 7  # Full House
                elif common[0] == 4:
                    strength = 8  # 4OAK
        # No possible way for unique_pairs to be 2 and be anything better then 2 pair
        elif unique_pairs == 2:
            if common[0] == hand[0] or common[1] == hand[0]:
                strength = 7  # Full House
            else:
                strength = 3  # Two pair

        # It is known that the other card has no commonalities on the board
        # So only test for this specific card
        if common_cards_1 >= 3:
            strength = 4  # 3OAK
            if unique_pairs == 1:
                strength = 4  # 3OAK - 2 values from common_cards_1 is the unique_pair on the board
            elif unique_pairs == 2:
                if card_common[0] == hand[0] or card_common[1] == hand[0]:
                    strength = 7  # Full House -> one unique_pair is common to hand ,one isnt
            if common_cards_1 == 4:
                strength = 8  # 4OAK

    elif common_cards_2 >= 2:  # At least 1 common card on the board with card2 in hand
        strength = 2  # At least a pair
        if unique_pairs == 1:
            if card_common[0] == hand[2]:
                strength = 4  # 3OAK
            else:
                strength = 3  # Two Pair At Least
                if common[0] == 3:
                    strength = 7  # Full House
                elif common[0] == 4:
                    strength = 8  # 4OAK
        elif unique_pairs == 2:
            if card_common[0] == hand[2] or card_common[1] == hand[2]:
                strength = 7  # Full House
            else:
                strength = 3  # Two pair
        if common_cards_2 >= 3:
            strength = 4  # 3OAK
            if unique_pairs == 1:
                strength = 4  # 3OAK - 2 values from common_cards_1 is the unique_pair on the board
            elif unique_pairs == 2:
                if card_common[0] == hand[2] or card_common[1] == hand[2]:
                    strength = 7  # Full House - one unique_pair is common to hand ,one isnt
            if common_cards_2 == 4:
                strength = 8  # 4OAK
    else:  # There are no pairs anywhere on the board with cards in hand
        strength = 1  # Just a high card - It should already be 1 to begin with
        # Last, we have to check if the board is paired in any way...
        if unique_pairs == 1:
            strength = 2  # Pair
            if common[0] >= 3:
                strength = 4  # 3OAK
                if common[0] == 4:
                    strength = 8  # 4OAK
        elif unique_pairs == 2:
            strength = 3  # Two Pair
            if common[0] == 3 or common[1] == 3:
                strength = 7  # Full House (Board will be a full house!)

    return strength


def straight(hand, ftr, return_highest=False):
    """Determine if the strength of the hand passed in is a straight (disregarding suits)."""
    strength = 1

    # Read card values from hand and board into the hand_numbered array and sort it
    sorted_array = hand_and_board(hand, ftr)

    straight = 1  # Technically the first card is the start of the straight
    highest_val = 5  # Lowest possible top straight value is a 5 (A - 5)
    for y in range(6):
        if sorted_array[y] + 1 == sorted_array[y + 1]:  # Straight condition
            straight += 1
            highest_val = sorted_array[y + 1]
        elif sorted_array[y] != sorted_array[y + 1]:
            straight = 1  # The straight was broken if it gets to here, so reset it
            if strength != 5:  # Reset highest value if we haven't found a straight yet
                highest_val = 5
        if straight >= 5:  # We found a straight!
            strength = 5  # Straight
        y += 1

    if strength == 1:  # We haven't found a straight yet
        strength = straight_ace_low(sorted_array)
        highest_val = 5  # The highest value possible at this point is 5.

    if return_highest:
        return highest_val

    return strength


def straight_ace_low(sorted_array):
    """Check if the array passed in is an ace low straight."""
    strength = 1

    if sorted_array[4] == 14 or sorted_array[5] == 14 or sorted_array[6] == 14:
        found_array = [1, 0, 0, 0, 0]
        for x in range(len(sorted_array)):
            if sorted_array[x] == 2:
                found_array[1] = 1
            elif sorted_array[x] == 3:
                found_array[2] = 1
            elif sorted_array[x] == 4:
                found_array[3] = 1
            elif sorted_array[x] == 5:
                found_array[4] = 1

        if found_array == [1, 1, 1, 1, 1]:
            strength = 5  # Straight

    return strength


def hand_and_board(hand, ftr):
    """Converts hand and board into numeric values (T to A), and returns sorted array."""
    hand_numbered = []

    # Convert face cards into numbers if needed
    combined_array = hand + ftr
    x = 0
    while x < len(combined_array):  # For the hand
        if combined_array[x] == 'T':
            hand_numbered.append(10)
        elif combined_array[x] == 'J':
            hand_numbered.append(11)
        elif combined_array[x] == 'Q':
            hand_numbered.append(12)
        elif combined_array[x] == 'K':
            hand_numbered.append(13)
        elif combined_array[x] == 'A':
            hand_numbered.append(14)
        else:
            hand_numbered.append(int(combined_array[x], base=10))
        x += 2

    return sorted(hand_numbered)


def flush(hand, ftr):
    """Determine if the strength of the hand passed in is a flush."""
    strength = 1  # Default

    # Testing the array passed in with suits
    suit = flush_suit(hand, ftr)

    # Now to check if any suit has >= 5 cards on board/hand
    if suit['♦'] >= 5 or suit['♥'] >= 5 or suit['♠'] >= 5 or suit['♣'] >= 5:
        strength = 6  # Flush

    return strength


def flush_suit(hand, ftr):
    """Sub function for flush."""
    combined_array = hand + ftr
    suit_arr = {'♦': 0, '♥': 0, '♠': 0, '♣': 0}

    for i in range(1, len(combined_array), 2):
        suit_arr[combined_array[i]] += 1

    return suit_arr


def flush_suit_value(suit_arr):
    """Extract the flush suit value from suit_arr."""
    if suit_arr['♦'] >= 5:
        return '♦'
    elif suit_arr['♥'] >= 5:
        return '♥'
    elif suit_arr['♠'] >= 5:
        return '♠'
    return '♣'


def straight_flush(hand, ftr):
    """Determine if the strength of the hand passed in is a straight or royal flush."""
    strength = 1

    # Check if the straight and flush are relating to the same 5 cards
    if straight(hand, ftr) == 5 and flush(hand, ftr) == 6:
        sorted_suits = sort_suits(hand, ftr)
        sorted_array = hand_and_board(hand, ftr)

        # Important -> To know the suit of the flush
        suit_arr = flush_suit(hand, ftr)
        flush_suit_var = flush_suit_value(suit_arr)

        sF = 1  # Straight Flush variable
        temp_array = sorted_array[:]
        temp_array_suits = sorted_suits[:]
        y = 0
        z = 0
        while y < 6 - z:
            if (sorted_array[y] + 1 == sorted_array[y + 1] and sorted_suits[y] == flush_suit_var
                    and sorted_suits[y + 1] == flush_suit_var):  # Straight Flush condition
                sF += 1
            elif sorted_suits[y] != sorted_suits[y + 1]:  # Remove the card not in the flush suit
                # Remove the un-needed suit and value
                if sorted_suits[y] != flush_suit_var:
                    suit_len = len(sorted_suits)
                    arr_len = len(sorted_array)
                    sorted_suits = sorted_suits[0:y] + sorted_suits[(y + 1):suit_len]
                    sorted_array = sorted_array[0:y] + sorted_array[(y + 1):arr_len]
                else:
                    suit_len = len(sorted_suits)
                    arr_len = len(sorted_array)
                    sorted_suits = sorted_suits[0:(y + 1)] + sorted_suits[(y + 2):suit_len]
                    sorted_array = sorted_array[0:(y + 1)] + sorted_array[(y + 2):arr_len]
                z += 1  # Want to loop 1 time less
                y -= 1
            y += 1

        if sF >= 5:  # We found a Straight Flush!
            strength = 9  # Straight Flush

        # Change the arrays back to normal
        sorted_array = temp_array[:]
        sorted_suits = temp_array_suits[:]

        if strength == 1:  # Check for ace low straight flush if not found yet
            strength = straight_flush_ace_low(sorted_array, sorted_suits)

        if strength == 9:  # Check for a royal flush if a straight flush exists
            strength = royal_flush(sorted_array, sorted_suits, flush_suit_var)

    return strength


def straight_flush_ace_low(sorted_array, sorted_suits):
    strength = 1

    # There could potentially be a straight flush with an ace at the beginning
    if sorted_array[4] == 14 or sorted_array[5] == 14 or sorted_array[6] == 14:
        if check_suits(sorted_array, sorted_suits):
            x = 0
            y = 0
            sF = 2  # We already know there's an ace and 2.
            while y < (x + 3):
                if (sorted_array[y] + 1 == sorted_array[y + 1] and
                        sorted_suits[y] == sorted_suits[y + 1]):
                    sF += 1
                elif sorted_array[y] == sorted_array[y + 1]:
                    x += 1
                    if x == 3:
                        x = 2
                y += 1
            if sF >= 5:
                strength = 9  # Straight Flush

    return strength


def royal_flush(sorted_array, sorted_suits, flush_suit_var):
    """Helper function for straight flush, checking for royal flush."""
    # Note - this function is only called when we know a straight flush exists
    strength = 9

    if sorted_array[0] == 10:  # Lowest card is a 10 - Must be a royal flush
        strength = 10
    elif sorted_array[1] == 10:  # Second lowest card in hand is a 10
        x = 1
        y = 1
        rF = 1
        while y < (x + 4):
            if sorted_array[y] + 1 == sorted_array[y + 1] and sorted_suits[y] == flush_suit_var:
                rF += 1
            elif sorted_array[y] == sorted_array[y + 1]:
                # In this case, we can just swap the two values and it will work
                sorted_array[y], sorted_array[y + 1] = sorted_array[y + 1], sorted_array[y]
                x += 1
                if x == 3:
                    x = 2
            y += 1
        if rF >= 5:
            strength = 10  # Royal Flush
    elif sorted_array[2] == 10:  # If a royal flush, last 5 cards must be it
        # --- Uglisest if statement ever, but it works :) ---
        if (sorted_array[3] == 11 and sorted_array[4] == 12 and sorted_array[5] == 13 and
                sorted_array[6] == 14 and sorted_suits[2] == flush_suit and
                sorted_suits[3] == flush_suit and sorted_suits[4] == flush_suit and
                sorted_suits[5] == flush_suit and sorted_suits[6] == flush_suit):
            strength = 10  # Royal Flush

    return strength


def check_suits(sorted_array, sorted_suits):
    """Sub function for straight/royal flush."""
    # This function is basically testing if the ace and two are of the same suit
    # And also makes sure that there is an ace and two in the common cards
    valid = False
    x = 0
    if sorted_array[4] == 14:  # There's three aces in common
        y = 0
    elif sorted_array[5] == 14:  # There's two aces in common
        y = 1
    else:
        y = 2  # There has to be at least one ace to get to this function

    while y < 3:
        while x < 3:
            if sorted_array[x] == 2:  # There must be at least 1 two in the 7 cards.
                if sorted_suits[x] == sorted_suits[y + 4]:
                    valid = True
            x += 1
        y += 1
        x = 0

    return valid


def sort_suits(hand, ftr):
    """Returns sorted suit array corresponding to the sorted_hand array"""
    suits_sorted = []
    sorted_array = hand_and_board(hand, ftr)
    combined = hand + ftr

    # First - change the court cards, 10 and ace values in the combined array
    x = 0
    while x <= 12:
        if combined[x] == 'T':
            combined[x] = chr(58)
        elif combined[x] == 'J':
            combined[x] = chr(59)
        elif combined[x] == 'Q':
            combined[x] = chr(60)
        elif combined[x] == 'K':
            combined[x] = chr(61)
        elif combined[x] == 'A':
            combined[x] = chr(62)
        x += 2

    # Second - test combined array against the 'sorted_array' array and correctly append
    # Into the suits_sorted array
    # Note, the 'ord' function will get the unicode value of a character
    # Using ord(combined[x]) - 48 will get the correct value
    x = 0
    y = 0
    while y < 7:  # Will loop 7 times
        while x < 14 - (2 * y):  # Will keep getting smaller based of how many times iterated
            if int(ord(combined[x])) - 48 == sorted_array[0]:
                # sorted_array[0] can stay 0 as the first element will be removed each time
                # After every pass, and the 0th place will be filled up again
                suits_sorted.append(combined[x + 1])  # The suit of that card
                # Slice the array to 'forget' about the two values we don't need anymore
                comLength = len(combined)  # To find the last element
                combined = combined[0:x] + combined[(x + 2):(comLength)]
                sorted_array.remove(sorted_array[0])
                x = 14  # Exit loop
            x += 2
        y += 1
        x = 0

    return suits_sorted


def overall_strength(hand, ftr):
    """Function which determines the overall strength of a hand. Accessed in the main function."""
    strength = pairs(hand, ftr)  # Get initial strength from pairs function

    a = flush(hand, ftr)
    b = straight(hand, ftr)
    c = straight_flush(hand, ftr)

    # If a, b or c contain higher values than strength, set strength to the higher value.
    if a > strength:
        strength = a

    if b > strength:
        strength = b

    if c > strength:
        strength = c

    return strength


def compare_strengths_main(winner, hands_to_compare, ftr, highest_strength_val,
                           overall_total_hands):
    """Sets up the framework for comparing strengths."""
    # Given the hands_to_compare list, compare all hands against each other and
    # tally up how many hands they BEAT. If one hand clearly beats every other
    # hand, it is the winner. If two hands beat other hands the same amount of times,
    # it's a split pot between those two hands.

    total_hands = len(hands_to_compare) // 4  # hands_to_compare contains two
    # card values and two suit values for each hand.

    # Initialising the array
    hands_beat = [0 for i in range(total_hands)]

    i = 0
    j = i + 1

    # Compare each hand against each other and tally up how many hands they beat
    while i < total_hands - 1:
        while j < total_hands:
            hand1 = hands_to_compare[i * 4:i * 4 + 4]
            hand2 = hands_to_compare[j * 4:j * 4 + 4]

            winner_val = compare_strengths(hand1, hand2, ftr, highest_strength_val)

            if winner_val == HAND1_WIN:
                hands_beat[i] += 1
            elif winner_val == HAND2_WIN:
                hands_beat[j] += 1

            j += 1
        i += 1
        j = i + 1

    highest_hands_beat = max(hands_beat)
    winner_indexes = []

    i = 0
    while i < overall_total_hands:
        if winner[i] == 1:
            winner_indexes.append(i)
        winner[i] = 0  # We want to reset the winner array to all 0 here
        i += 1

    i = 0
    while i < total_hands:
        if hands_beat[i] == highest_hands_beat:
            winner[winner_indexes[i]] = 1  # Set appropriate winner index to 1.
        i += 1

    return winner


def compare_strengths(hand1, hand2, ftr, strength):
    """Function for comparing two hands of the same strength."""
    winner = 0

    sorted_hand1 = hand_and_board(hand1, ftr)
    sorted_hand2 = hand_and_board(hand2, ftr)

    if strength == 1:  # High Card
        winner = compare_strength_one(sorted_hand1, sorted_hand2)
    elif strength == 2:  # Pair
        winner = compare_strength_two(sorted_hand1, sorted_hand2)
    elif strength == 3:  # Two Pair
        winner = compare_strength_three(sorted_hand1, sorted_hand2)
    elif strength == 4:  # Three Of A Kind
        winner = compare_strength_four(sorted_hand1, sorted_hand2)
    elif strength == 5:  # Straight
        winner = compare_strength_five(hand1, hand2, ftr)
    elif strength == 6:  # Flush
        winner = compare_strength_six(hand1, hand2, ftr)
    elif strength == 7:  # Full House
        winner = compare_strength_seven(sorted_hand1, sorted_hand2)
    elif strength == 8:  # 4OAK
        winner = compare_strength_eight(sorted_hand1, sorted_hand2)
    elif strength == 9:  # Straight Flush
        winner = compare_strength_nine(hand1, hand2, ftr, sorted_hand1, sorted_hand2)
    else:  # Royal Flush - ONLY possible way this occurs is if the royal flush is on the board! o-o
        winner = SPLIT_POT

    return winner


def get_kickers(sorted_hand, amount):
    """Gets the top 'amount' of kickers from sorted hand and returns a list of them."""
    # The first index in the returned list will be the highest value
    return [sorted_hand[-(i + 1)] for i in range(amount)]


def compare_strength_one(sorted_hand1, sorted_hand2):
    """Compare two hands of strength one - High Card."""
    # Since strength is 1 (highest card), all 5 cards are kickers.
    hand1_kickers = get_kickers(sorted_hand1, 5)
    hand2_kickers = get_kickers(sorted_hand2, 5)

    for i in range(5):
        if hand1_kickers[i] != hand2_kickers[i]:  # We found a winner
            return HAND1_WIN if hand1_kickers[i] > hand2_kickers[i] else HAND2_WIN

    return SPLIT_POT


def compare_strength_two(sorted_hand1, sorted_hand2):
    """Compare two hands of strength two - Pair."""
    # Find the indexes of the two pair values
    pair_val1 = get_pair_val(sorted_hand1)
    pair_val2 = get_pair_val(sorted_hand2)

    if pair_val1 > pair_val2:
        return HAND1_WIN
    elif pair_val1 < pair_val2:
        return HAND2_WIN

    # We refer to the three kickers left here to determine the winner
    hand1_not_pair = [sorted_hand1[x] for x in range(7) if sorted_hand1[x] != pair_val1]
    hand2_not_pair = [sorted_hand2[x] for x in range(7) if sorted_hand2[x] != pair_val2]

    hand1_kickers = get_kickers(hand1_not_pair, 3)
    hand2_kickers = get_kickers(hand2_not_pair, 3)

    for i in range(3):
        if hand1_kickers[i] != hand2_kickers[i]:  # We found a winner
            return HAND1_WIN if hand1_kickers[i] > hand2_kickers[i] else HAND2_WIN

    return SPLIT_POT


def get_pair_val(sorted_hand):
    """Gets the value of a pair and returns it."""
    pair_val = 0  # Should never stay 0
    for x in range(len(sorted_hand) - 1):
        if sorted_hand[x] == sorted_hand[x + 1]:
            pair_val = sorted_hand[x]

    return pair_val


def compare_strength_three(sorted_hand1, sorted_hand2):
    """Compare two hands of strength three - Two Pair."""
    # Refer to the two pairs, and if needed, the remaining kicker.

    hand1_pair_vals = [-1, -1]
    hand2_pair_vals = [-1, -1]

    for x in range(6):
        if hand1_pair_vals[0] == -1 and sorted_hand1[x] == sorted_hand1[x + 1]:
            hand1_pair_vals[0] = sorted_hand1[x]
        elif hand1_pair_vals[1] == -1 and sorted_hand1[x] == sorted_hand1[x + 1]:
            hand1_pair_vals[1] = sorted_hand1[x]
        elif sorted_hand1[x] == sorted_hand1[x + 1]:
            # If it gets to here, we find a third higher pair somewhere
            # Therefore, we don't care about the lowest pair anymore
            hand1_pair_vals[0] = hand1_pair_vals[1]
            hand1_pair_vals[1] = sorted_hand1[x]

        if hand2_pair_vals[0] == -1 and sorted_hand2[x] == sorted_hand2[x + 1]:
            hand2_pair_vals[0] = sorted_hand2[x]
        elif hand2_pair_vals[1] == -1 and sorted_hand2[x] == sorted_hand2[x + 1]:
            hand2_pair_vals[1] = sorted_hand2[x]
        elif sorted_hand2[x] == sorted_hand2[x + 1]:
            hand2_pair_vals[0] = hand2_pair_vals[1]
            hand2_pair_vals[1] = sorted_hand2[x]

    # Find the higher and lower pair for each hand
    higher1 = max(hand1_pair_vals)
    lower1 = min(hand1_pair_vals)
    higher2 = max(hand2_pair_vals)
    lower2 = min(hand2_pair_vals)

    # First - check higher pairs of the two. If higher ones same, check lower ones
    if higher1 > higher2:
        return HAND1_WIN
    elif higher1 < higher2:
        return HAND2_WIN
    elif lower1 > lower2:
        return HAND1_WIN
    elif lower1 < lower2:
        return HAND2_WIN

    # Both hands have the same two pair - refer to the final kicker
    kickers1 = [sorted_hand1[x] for x in range(7) if sorted_hand1[x] not in hand1_pair_vals]
    kickers2 = [sorted_hand2[x] for x in range(7) if sorted_hand2[x] not in hand2_pair_vals]

    # We know sorted_hand is sorted, So just take item at end of the list for largest kicker
    kicker1 = kickers1[-1]
    kicker2 = kickers2[-1]

    if kicker1 > kicker2:
        return HAND1_WIN
    elif kicker1 < kicker2:
        return HAND2_WIN

    return SPLIT_POT  # same kicker and same two pair


def compare_strength_four(sorted_hand1, sorted_hand2):
    """Compare two hands of strength four - Three Of A Kind."""
    # Find which 3OAK has the higher value. If same, refer to 2 kickers
    three_val1 = get_three_val(sorted_hand1)
    three_val2 = get_three_val(sorted_hand2)

    if three_val1 > three_val2:
        return HAND1_WIN
    elif three_val1 < three_val2:
        return HAND2_WIN

    # both 3OAK values are the same - refer to 2 remaining kickers for each hand
    kickers1 = [sorted_hand1[x] for x in range(7) if sorted_hand1[x] != three_val1]
    kickers2 = [sorted_hand2[x] for x in range(7) if sorted_hand2[x] != three_val2]

    hand1_kickers = get_kickers(kickers1, 2)
    hand2_kickers = get_kickers(kickers2, 2)

    for i in range(2):
        if hand1_kickers[i] != hand2_kickers[i]:  # We found a winner
            return HAND1_WIN if hand1_kickers[i] > hand2_kickers[i] else HAND2_WIN

    return SPLIT_POT  # Both kickers are the same


def get_three_val(sorted_hand):
    """Gets the value of the three of a kind and returns it."""
    three_val = 0  # Should never stay 0
    for x in range(len(sorted_hand) - 2):
        if sorted_hand[x] == sorted_hand[x + 1] == sorted_hand[x + 2]:
            three_val = sorted_hand[x]
    return three_val


def compare_strength_five(hand1, hand2, ftr):
    """Compare two hands of strength five - Straight."""
    # There can never be 2 different straights on the board - find which hand has higher top value
    highest_value1 = straight(hand1, ftr, True)
    highest_value2 = straight(hand2, ftr, True)

    if highest_value1 > highest_value2:
        return HAND1_WIN
    elif highest_value1 < highest_value2:
        return HAND2_WIN

    return SPLIT_POT


def compare_strength_six(hand1, hand2, ftr):
    """Compare two hands of strength six - Flush."""
    flush_list = flush_suit(hand1, ftr)  # Suit will be the same for hand 1 and hand 2
    suit_of_flush = flush_suit_value(flush_list)

    hand1_top5 = get_top_flush_values(hand1, ftr, suit_of_flush)
    hand2_top5 = get_top_flush_values(hand2, ftr, suit_of_flush)

    for i in range(5):  # 5 cards in a flush that we care about
        if hand1_top5[i] != hand2_top5[i]:
            return HAND1_WIN if hand1_top5[i] > hand2_top5[i] else HAND2_WIN

    return SPLIT_POT


def get_top_flush_values(hand, ftr, suit_of_flush):
    """Return the top flush values of a hand/ftr combination."""
    suits = sort_suits(hand, ftr)
    values = hand_and_board(hand, ftr)
    top_flush_suit_values = []

    for i in range(len(values)):
        if suits[i] == suit_of_flush:
            top_flush_suit_values.append(values[i])

    return (sorted(top_flush_suit_values))[::-1]  # Return a reverse sorted array


def compare_strength_seven(sorted_hand1, sorted_hand2):
    """Compare two hands of strength seven - Full House."""
    three_val1 = get_three_val(sorted_hand1)
    three_val2 = get_three_val(sorted_hand2)

    if three_val1 > three_val2:
        return HAND1_WIN
    elif three_val1 < three_val2:
        return HAND2_WIN

    # If it gets to here, 3OAK vals are equal, so refer to the remaining pair (no kickers)
    remaining_cards1 = [x for x in sorted_hand1 if x != three_val1]
    remaining_cards2 = [x for x in sorted_hand2 if x != three_val2]

    pair_val1 = get_pair_val(remaining_cards1)
    pair_val2 = get_pair_val(remaining_cards2)

    if pair_val1 > pair_val2:
        return HAND1_WIN
    elif pair_val1 < pair_val2:
        return HAND2_WIN

    return SPLIT_POT


def compare_strength_eight(sorted_hand1, sorted_hand2):
    """Compare two hands of strength eight - Four Of A Kind."""
    four_val1 = get_four_val(sorted_hand1)
    four_val2 = get_four_val(sorted_hand2)

    if four_val1 > four_val2:
        return HAND1_WIN
    elif four_val1 < four_val2:
        return HAND2_WIN

    # Refer to the final kicker here to determine the winner (or split pot)
    kickers1 = [sorted_hand1[x] for x in range(7) if sorted_hand1[x] != four_val1]
    kickers2 = [sorted_hand2[x] for x in range(7) if sorted_hand2[x] != four_val2]

    # We know sorted_hand is sorted, So just take item at end of the list for largest kicker
    kicker1 = kickers1[-1]
    kicker2 = kickers2[-1]

    if kicker1 > kicker2:
        return HAND1_WIN
    elif kicker1 < kicker2:
        return HAND2_WIN

    return SPLIT_POT  # same kicker and same two pair


def get_four_val(sorted_hand):
    """Gets the value of the four of a kind and returns it."""
    four_value = 0  # Should never stay 0.
    for x in range(len(sorted_hand) - 3):
        if sorted_hand[x] == sorted_hand[x + 1] == sorted_hand[x + 2] == sorted_hand[x + 3]:
            four_value = sorted_hand[x]
    return four_value


def compare_strength_nine(hand1, hand2, ftr, sorted_hand1, sorted_hand2):
    """Compare two hands of strength nine - Straight Flush."""
    # There will never be two different straight flushes, so find the one with the higher
    # Value in it. Cannot split in this one unless straight flush is on board

    sorted_suits1 = sort_suits(hand1, ftr)
    sorted_suits2 = sort_suits(hand2, ftr)
    suit_arr = flush_suit(hand1, ftr)
    fs = flush_suit_value(suit_arr)  # flush suit

    hs1 = straight(hand1, ftr, True)  # Highest straight value 1
    hs2 = straight(hand2, ftr, True)  # Highest straight value 2
    highest_sf_value1 = ensure_highest_sf_value(sorted_hand1, sorted_suits1, hs1, fs)
    highest_sf_value2 = ensure_highest_sf_value(sorted_hand2, sorted_suits2, hs2, fs)

    if highest_sf_value1 > highest_sf_value2:
        return HAND1_WIN
    elif highest_sf_value1 < highest_sf_value2:
        return HAND2_WIN

    return SPLIT_POT


def ensure_highest_sf_value(sorted_hand, sorted_suits, highest_value, flush_suit_var):
    """Ensures that highest straight value is within the straight flush."""
    highest_val_in_sf = False
    while not highest_val_in_sf:
        for i in range(4, 7):  # Only from index 4 to 6 as looking for highest straight val
            if sorted_hand[i] == highest_value and sorted_suits[i] == flush_suit_var:
                highest_val_in_sf = True
        if not highest_val_in_sf:
            highest_value -= 1

    return highest_value
