import engine as engine
import time  # To allow the program to 'sleep' for a specific amount of time
import os  # Used to clear screen
import random


def main():
    '''The main function for the survival poker program.'''
    # Preparing for the game
    score = 0
    lives = 5
    cards = generate_cards()
    hand_amount = get_valid_hand_amount()

    while lives > 0:
        # Generate new hands and ftr (flop, turn, river)
        cards_used = []
        hands_array = generate_hands(cards_used, cards, hand_amount)
        ftr = generate_ftr(cards_used, cards)

        # Find the strengths of each hand and then determine the winner of the round
        strengths = get_strengths(hands_array, ftr, hand_amount)
        winner = determine_winner(hands_array, ftr, strengths)

        # Print the interface, get users choice of hand to win, update score and lives
        print_interface(lives, score, hand_amount, hands_array)
        hand_choice = get_valid_hand_choice(hand_amount)
        print_ftr(ftr)
        score, lives = print_winner(winner, hand_choice, score, lives, strengths)

        input("Press enter to continue! ")

        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

    print("Unfortunately, you have ran out of lives!")
    print("Your final score was:", score)

    input("")


def testing_function(hand_amount, hands_array, ftr):
    """The testing function called when the tests.py file is ran with pytest."""
    strengths = get_strengths(hands_array, ftr, hand_amount)
    winner = determine_winner(hands_array, ftr, strengths)
    winning_hands = get_winning_hands(winner)
    return (winning_hands, strengths)


def generate_cards():
    """Generate the 52 Cards and store it in the cards array passed in."""
    cards = []
    suit = {1: '♦', 2: '♥', 3: '♠', 4: '♣'}

    for count in range(1, 5):
        # Aces:
        cards.append('A')
        cards.append(suit[count])

        # Numbers 2-9:
        for number in range(2, 10):
            cards.append(chr(48 + number))
            cards.append(suit[count])

        # Ten & Court Cards:
        cards.append('T')
        cards.append(suit[count])
        cards.append('J')
        cards.append(suit[count])
        cards.append('Q')
        cards.append(suit[count])
        cards.append('K')
        cards.append(suit[count])

    return cards


def generate_hands(cards_used, cards, hand_amount):
    """Generate the hands, the amount determined by the value of 'hand_amount' parameter."""
    hands_array = []
    for i in range(0, hand_amount):
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

    return hands_array


def generate_ftr(cards_used, cards):
    """Generate the flop, turn and river."""
    ftr = []
    x = 0
    while x < 5:  # Always 5 cards in the flop, turn and river
        card = (random.randint(0, 51) * 2)
        if is_duplicate(cards_used, cards[card], cards[card + 1]) == 0:
            ftr.append(cards[card])
            ftr.append(cards[card + 1])
            cards_used.append(cards[card])
            cards_used.append(cards[card + 1])
            x += 1

    return ftr


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


def get_valid_hand_amount():
    """Get a valid hand amount, being between 1 and 9."""
    hand_amount = 0

    while hand_amount == 0:
        hand_amount = input("How many hands would you like to play with in this session? ")
        if len(hand_amount) != 1:
            print("Please choose a valid hand amount.")
            hand_amount = 0
        else:
            ord_hand_amount = ord(hand_amount)  # 'ord' translates character into unicode value.
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

    print()  # To keep the interface neat
    return int(hand_choice)


def get_strengths(hands_array, ftr, hand_amount):
    """Obtain the strength values of all the hands."""
    strengths = []
    i = 0
    while i < hand_amount:
        start_index = 4 * i  # How far we're going into the hands_array array.
        end_index = start_index + 4
        hand = hands_array[start_index:end_index]  # The hand which we want to find the strength of.
        strengths.append(engine.overall_strength(hand, ftr))
        i += 1

    return strengths


def get_winning_hands(winner):
    """Calculates the winning hands array."""
    # 'winner' array contains either 1 or 0. If winner[i] = 1, then hand i + 1 is a winner.
    winning_hands = [i + 1 for i in range(len(winner)) if winner[i] == 1]
    return winning_hands


def get_winning_strength(strength):
    """For printing purposes, returning the winning strength."""
    strengths = {
        1: "High Card",
        2: "Pair",
        3: "Two Pair",
        4: "Three Of A Kind",
        5: "Straight",
        6: "Flush",
        7: "Full House",
        8: "Four Of A Kind",
        9: "Straight Flush",
        10: "Royal Flush"
    }
    return strengths[strength]


def print_interface(lives, score, hand_amount, hands_array):
    """Prints the game interface, such as the rules, hands and ftr."""
    print("------------------ Welcome to Survival Poker ------------------")
    print("• The aim of the game is to choose a hand and hope it wins!")
    print("• You get 5 lives.")
    print("• If your hand loses, you lose a life.")
    print("• If there is a split pot, you don't lose a life or gain any score.")
    print("• If your hand wins, your score increases by one.")
    print(f"• To choose a hand, type a number between 1 and {hand_amount}.")
    print("\n--- Scoreboard ---")
    print(f"Lives: {lives}")
    print(f"Score: {score}\n")

    # Print 'Hand' and the hand number, seperated by a tab (4 spaces)
    for i in range(1, hand_amount + 1):
        print(f"Hand{i}    ", end="") if i != hand_amount else print(f"Hand{i}")

    # Print the actual values of the hands directly below it's hand 'title'
    index = 0
    for i in range(1, hand_amount + 1):
        print(f"{hands_array[index]}{hands_array[index + 1]}|"
              f"{hands_array[index + 2]}{hands_array[index + 3]}", end="")
        print("    ", end="") if i != hand_amount else print()
        index += 4

    print()  # To keep the interface neat


def print_ftr(ftr):
    """Prints the flop, turn and river."""
    print("Dealer is getting ready...\n")

    time.sleep(2)
    print(f"{ftr[0]}{ftr[1]} {ftr[2]}{ftr[3]} {ftr[4]}{ftr[5]} ", end="")
    time.sleep(2)
    print(f"{ftr[6]}{ftr[7]} ", end="")
    time.sleep(2)
    print(f"{ftr[8]}{ftr[9]}\n")
    time.sleep(2)


def print_winner(winner, hand_choice, score, lives, strengths):
    """Prints the winner or split winners based of values within the winner array."""
    winning_hands = get_winning_hands(winner)
    highest_strength_val = max(strengths)
    winning_reason = get_winning_strength(highest_strength_val)

    if len(winning_hands) == 1:
        print(f"The Winner is Hand {winning_hands[0]}, with a {winning_reason}.")
        if hand_choice in winning_hands:
            print("Congratulations, you chose the correct hand!")
            score += 1
        else:
            print("Unfortunately, you did not choose the correct hand.")
            lives -= 1
    else:
        print("There was a Split Pot between ", end="")
        for hand in winning_hands:
            print(f"{hand}, ", end="")
        print(f"with a {winning_reason}.")

        if hand_choice in winning_hands:
            print("You chose one of these hands. No change occurs.")
        else:
            print("Unfortunately, you did not choose one of the correct hands.")
            lives -= 1

    print()  # For neat interface purposes

    return (score, lives)


def determine_winner(hands_array, ftr, strengths):
    """Based off the strength values of the cards, determine the winner."""
    winner = []
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

    return winner


if __name__ == '__main__':
    main()
