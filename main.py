import SurvivalPokerEngine as engine
import time  # To allow the program to 'sleep' for a specific amount of time
import os  # Used for clearing the screen in the command prompt (cls)
import random


def main(*args):
    '''
    Detect which level of 'strength' each hand is when comparing to flop, turn, river.
    If clear winner, no further calculation needed. If not, compare the strengths of the hands.

    The 10 strength values of poker hands:
    1. High Card
    2. Pair
    3. Two Pair
    4. Three Of A Kind
    5. Straight
    6. Flush
    7. Full House
    8. Four Of A Kind
    9. Straight Flush
    10. Royal Flush
    '''

    cards = []  # Contains the 52 cards
    generate_cards(cards)  # Generates the 52 cards

    score = 0  # Rounds 'survived'
    lives = 5  # Beginning lives

    if not args:  # If not testing
        hand_amount = get_valid_hand_amount()

    while lives > 0:
        if args:  # When testing
            if len(args) != 3:
                print("Incorrect number of arguments passed for testing.")
                quit()
            hand_amount = args[0]
            hands_array = args[1]
            ftr = args[2]
        else:  # When not testing
            # Generate new hands and ftr for each game loop - hence re-initialise the arrays
            hands_array = []
            cards_used = []
            ftr = []
            generate_hands(hands_array, hand_amount, cards_used, cards)
            generate_ftr(ftr, cards_used, cards)

        strengths = []
        get_strengths(strengths, hands_array, ftr, hand_amount)

        winner = []
        determine_winner(hands_array, strengths, ftr, winner)

        if args:  # When testing
            result = get_winning_hands(winner)
            return result[0]  # contains winning_hands
        else:  # When not testing
            print_interface(lives, score, hand_amount, hands_array)
            print()
            hand_choice = get_valid_hand_choice(hand_amount)
            print()
            print_ftr(ftr)
            print()
            score, lives = print_winner(winner, hand_choice, score, lives, strengths)
            print()

        input("Press enter to continue! ")

        os.system('cls')  # works for windows -> Clears screen on the command prompt

    print("Unfortunately, you have ran out of lives!")
    print("Your final score was:", score)

    input("")


def get_valid_hand_amount():
    """Get a valid hand amount, being between 1 and 9."""
    hand_amount = 0

    while hand_amount == 0:
        hand_amount = input("How many hands would you like to play with in this session? ")
        if len(hand_amount) != 1:
            print("Please choose a valid hand amount.")
            hand_amount = 0
        else:
            ord_hand_amount = ord(hand_amount)  # ord translate character into unicode value.
            # unicode value of 48 is the integer 0.
            if ord_hand_amount < 49 or ord_hand_amount > 57:
                print("Please choose a valid hand amount.")
                hand_amount = 0

    return int(hand_amount)


def get_valid_hand_choice(hand_amount):
    hand_choice = 0

    while hand_choice == 0:
        hand_choice = input("Choose a hand to win: ")
        if len(hand_choice) != 1:
            print("Please make a valid hand choice.")
            hand_choice = 0
        else:
            ord_hand_choice = ord(hand_choice)
            if ord_hand_choice < 49 or ord_hand_choice > 48 + hand_amount:
                print("Please make a valid hand choice.")
                hand_choice = 0

    return int(hand_choice)


def generate_cards(cards):
    """Generate the 52 Cards."""
    suit = 1  # Diamonds = 1, Hearts = 2, Spades = 3, Clubs = 4
    number = 2

    while suit <= 4:
        # Aces:
        cards.append('A')
        if suit == 1:
            cards.append('♦')
        elif suit == 2:
            cards.append('♥')
        elif suit == 3:
            cards.append('♠')
        else:
            cards.append('♣')

        # Numbers 2-9:
        while number <= 9:
            cards.append(chr(48 + number))
            if suit == 1:
                cards.append('♦')
            elif suit == 2:
                cards.append('♥')
            elif suit == 3:
                cards.append('♠')
            else:
                cards.append('♣')
            number += 1

        # Court Cards & Ten:
        if suit == 1:
            cards.append('T')
            cards.append('♦')
            cards.append('J')
            cards.append('♦')
            cards.append('Q')
            cards.append('♦')
            cards.append('K')
            cards.append('♦')
        elif suit == 2:
            cards.append('T')
            cards.append('♥')
            cards.append('J')
            cards.append('♥')
            cards.append('Q')
            cards.append('♥')
            cards.append('K')
            cards.append('♥')
        elif suit == 3:
            cards.append('T')
            cards.append('♠')
            cards.append('J')
            cards.append('♠')
            cards.append('Q')
            cards.append('♠')
            cards.append('K')
            cards.append('♠')
        else:
            cards.append('T')
            cards.append('♣')
            cards.append('J')
            cards.append('♣')
            cards.append('Q')
            cards.append('♣')
            cards.append('K')
            cards.append('♣')

        suit += 1
        number = 2

    return cards


def generate_hands(hands_array, hand_amount, cards_used, cards):
    """Generate the hands, the amount determined by the value of 'hand_amount' parameter."""
    i = 1  # Hands starts at 1.

    while i <= hand_amount:
        x = 0
        while x < 2:
            card = (random.randint(0, 51) * 2)

            # is_duplicate returns 0 if no duplicates found.
            if is_duplicate(cards_used, cards[card], cards[card + 1]) == 0:
                hands_array.append(cards[card])
                hands_array.append(cards[card + 1])
                cards_used.append(cards[card])
                cards_used.append(cards[card + 1])
                x += 1
        i += 1


def generate_ftr(ftr, cards_used, cards):
    """Generate the flop, turn and river."""
    x = 0

    while x < 5:  # Always 5 cards in the flop, turn and river
        card = (random.randint(0, 51) * 2)
        if is_duplicate(cards_used, cards[card], cards[card + 1]) == 0:
            ftr.append(cards[card])
            ftr.append(cards[card + 1])
            cards_used.append(cards[card])
            cards_used.append(cards[card + 1])
            x += 1


def get_strengths(strengths, hands_array, ftr, hand_amount):
    """Obtain the strength values of all the hands."""
    i = 0
    while i < hand_amount:
        start_index = 4 * i  # How far we're going into the hands_array array.
        end_index = start_index + 4
        hand = hands_array[start_index:end_index]  # The hand which we want to find the strength of.
        strengths.append(engine.overall_strength(hand, ftr))
        i += 1


def is_duplicate(array, newValue, newSuit):
    """Testing for duplicate cards in the same array."""
    i = 0
    length = len(array)
    dup = 0  # 0 for false, 1 for true

    if length <= 2:
        return dup  # First card cannot be a duplicate

    while i < length:
        if array[i] == newValue and array[i + 1] == newSuit:
            dup = 1  # Duplicate card
            break
        i += 2

    return dup


def determine_winner(hands_array, strengths, ftr, winner):
    """Based off the strength values of the cards, determine the winner."""
    total_hands = len(strengths)  # Alternative to the hand_amount variable
    highest_strength_val = max(strengths)

    i = 0
    same_strength_hands = 0
    hands_to_compare = []
    while i < total_hands:  # Find how many hands have the highest strength
        if strengths[i] == highest_strength_val:
            winner.append(1)
            same_strength_hands += 1
            for j in range(i * 4, (i * 4) + 4):  # Incase we have hands of the same strength.
                hands_to_compare.append(hands_array[j])
        else:
            winner.append(0)  # Else set it to 0 which makes it easy to disregard non strong hands.
        i += 1

    if same_strength_hands >= 2:
        winner = engine.compare_strengths_main(winner, hands_to_compare, ftr,
                                               highest_strength_val, total_hands)


def print_interface(lives, score, hand_amount, hands_array):
    """Prints the game interface, such as the rules, hands and ftr."""
    print("------------------ Welcome to Survival Poker ------------------")
    print("• The aim of the game is to choose a hand and hope it wins!")
    print("• You get 5 lives.")
    print("• If your hand loses, you lose a life.")
    print("• If there is a split pot, you don't lose a life or gain any score.")
    print("• If your hand wins, your score increases by one.")
    print(f"• To choose a hand, type a number between 1 and {hand_amount}.")
    print()
    print("--- Scoreboard ---")
    print("Lives: " + str(lives))  # these are integers to begin, cannot concatenate ints
    print("Score: " + str(score))

    print()

    i = 1
    while i <= hand_amount:
        print(f"Hand{i}", end="")
        if i < hand_amount:  # Don't print this for the last hand
            print("    ", end="")
        else:
            print()  # Acts as a new line after final hand printed
        i += 1

    i = 1
    index = 0
    while i <= hand_amount:
        print(hands_array[index] + hands_array[index + 1] + "|" +
              hands_array[index + 2] + hands_array[index + 3], end="")
        if i < hand_amount:
            print("    ", end="")
        else:
            print()
        index += 4
        i += 1


def print_ftr(ftr):
    """Prints the flop, turn and river."""
    print("Dealer is getting ready...")
    print()

    time.sleep(2)
    print(ftr[0] + ftr[1] + " " + ftr[2] + ftr[3] + " " + ftr[4] + ftr[5] + " ", end="")
    time.sleep(2)
    print(ftr[6] + ftr[7] + " ", end="")
    time.sleep(2)
    print(ftr[8] + ftr[9])
    time.sleep(2)


def print_winner(winner, hand_choice, score, lives, strengths):
    """Prints the winner or split winners based of values within the winner array."""
    winning_hands, hands_won = get_winning_hands(winner)
    highest_strength_val = max(strengths)
    winning_reason = engine.print_winning_strength(highest_strength_val)

    if hands_won == 1:
        print("The Winner is Hand", winning_hands[0], "with a", winning_reason + ".")
        if hand_choice in winning_hands:
            print("Congratulations, you chose the correct hand!")
            score += 1
        else:
            print("Unfortunately, you did not choose the correct hand.")
            lives -= 1
    else:  # hands_won >= 2
        print("There was a Split Pot between Hands: ", end="")
        for hand in winning_hands:
            print(f"{hand} ", end="")
        print("with a", winning_reason + ".")

        if hand_choice in winning_hands:
            print("You chose one of these hands. No change occurs.")
        else:
            print("You did not choose one of these hands.")
            lives -= 1

    return score, lives


def get_winning_hands(winner):
    """Calculates the winning hands array."""
    # winner is an array with values containing either 1 or 0.
    # If winner[i] = 1, then hand i + 1 is a winner.
    i = 0
    hands_won = 0
    winning_hands = []

    while i < len(winner):
        if winner[i] == 1:
            hands_won += 1
            winning_hands.append(i + 1)  # i + 1 is the HAND that was chosen. Not index.
        i += 1

    return winning_hands, hands_won


if __name__ == '__main__':
    main()
