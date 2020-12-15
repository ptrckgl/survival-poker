import main as main
import pytest

# Commands to run
# python3 -m pytest tests.py
# coverage run -m pytest tests.py
# coverage report

# ♦ ♥ ♠ ♣

# assert main.main(hand_amount, hands_array, ftr) == [1] means
# that hand 1 should be the winning hand. If it was asserting to
# [2, 4], it means there should be a split pot between hands 2 and 4.

# --- Strength 1 Tests: High Card ---


def test_high_card_win():
    """Testing high card win."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', '9', '♠', '5', '♦', '2', '♠', 'J', '♦']
    ftr = ['3', '♦', 'T', '♦', '7', '♥', 'K', '♦', '8', '♠']
    assert main.testing_function(hand_amount, hands_array, ftr) == [3]


def test_high_card_split_pot():
    """Testing high card split pot."""
    hand_amount = 3
    hands_array = ['4', '♣', 'J', '♣', '9', '♠', '5', '♦', '2', '♠', 'J', '♦']
    ftr = ['3', '♦', 'T', '♦', '7', '♥', 'K', '♦', '8', '♠']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1, 3]


def test_high_cards_on_board():
    """Testing the board containing all five high cards."""
    hand_amount = 2
    hands_array = ['4', '♣', '2', '♣', '6', '♠', '5', '♠']
    ftr = ['K', '♦', 'Q', '♦', 'J', '♦', '8', '♦', 'A', '♥']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1, 2]


# --- Strength 2 Tests: Pair ---


def test_pocket_aces():
    """Testing a simple pocket aces win."""
    hand_amount = 3
    hands_array = ['A', '♣', 'A', '♠', '3', '♥', '5', '♠', '6', '♥', 'T', '♥']
    ftr = ['K', '♦', 'Q', '♦', 'J', '♦', '8', '♦', '7', '♥']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1]


def test_pair_on_board_high_card():
    """Testing pair on the board with a high card win."""
    hand_amount = 3
    hands_array = ['4', '♣', '5', '♥', '3', '♥', '5', '♠', '6', '♥', 'T', '♥']
    ftr = ['K', '♦', 'K', '♣', 'J', '♦', '8', '♦', '7', '♥']
    assert main.testing_function(hand_amount, hands_array, ftr) == [3]


def test_split_pair():
    """Testing two pocket pairs split pot."""
    hand_amount = 2
    hands_array = ['4', '♣', '4', '♥', '4', '♦', '4', '♠']
    ftr = ['K', '♦', '2', '♣', 'J', '♦', '8', '♦', '7', '♥']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1, 2]


# --- Strength 3 Tests: Two Pair ---


def test_won_two_pair():
    """Testing a won two pair hand."""
    hand_amount = 3
    hands_array = ['3', '♣', '4', '♥', '6', '♦', '7', '♠', '8', '♠', '9', '♠']
    ftr = ['Q', '♦', '8', '♣', '9', '♦', '4', '♦', '3', '♥']
    assert main.testing_function(hand_amount, hands_array, ftr) == [3]


def test_split_two_pair():
    """Testing a split two pair on the whole board."""
    hand_amount = 3
    hands_array = ['4', '♦', '6', '♥', 'K', '♥', 'Q', '♦', 'J', '♠', 'T', '♠']
    ftr = ['A', '♣', '9', '♥', '5', '♣', '5', '♥', '9', '♣']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1, 2, 3]


def test_won_two_pair_using_kicker():
    """Testing a won two pair using a kicker."""
    hand_amount = 3
    hands_array = ['4', '♦', '6', '♥', 'K', '♥', 'Q', '♦', 'J', '♠', 'T', '♠']
    ftr = ['A', '♣', 'A', '♥', '5', '♣', '5', '♥', '9', '♣']
    assert main.testing_function(hand_amount, hands_array, ftr) == [2]


# --- Strength 4 Tests: Three Of A Kind ---


def test_three_of_a_kind():
    """Testing Three Of a Kind win."""
    hand_amount = 3
    hands_array = ['A', '♦', 'A', '♥', 'K', '♦', 'K', '♥', 'Q', '♦', 'Q', '♥']
    ftr = ['A', '♣', '3', '♣', '5', '♠', '7', '♣', '9', '♣']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1]


def test_three_of_a_kind_win_kicker():
    """Testing a three of a kind win from the two kickers."""
    hand_amount = 3
    hands_array = ['9', '♦', 'K', '♥', 'K', '♦', '8', '♥', 'Q', '♦', '6', '♥']
    ftr = ['A', '♣', 'A', '♦', '5', '♠', '7', '♣', 'A', '♥']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1]


def test_three_of_a_kind_split_pot():
    """Testing a split against two hands for three of a kind."""
    hand_amount = 3
    hands_array = ['9', '♦', 'K', '♥', 'Q', '♠', '8', '♥', 'Q', '♥', '6', '♥']
    ftr = ['Q', '♣', 'Q', '♦', '5', '♠', 'T', '♣', 'A', '♥']
    assert main.testing_function(hand_amount, hands_array, ftr) == [2, 3]


# --- Strength 5 Tests: Straight ---


def test_split_straight():
    """Testing Split Straight."""
    hand_amount = 3
    hands_array = ['J', '♣', 'Q', '♣', '9', '♠', '5', '♦', '2', '♠', 'J', '♦']
    ftr = ['6', '♦', 'T', '♦', 'Q', '♥', 'K', '♦', 'A', '♠']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1, 3]


def test_straight_ten_ace():
    hand_amount = 3
    hands_array = ['J', '♣', 'Q', '♣', 'T', '♠', '5', '♦', '3', '♠', '4', '♦']
    ftr = ['T', '♦', 'K', '♦', '4', '♥', 'A', '♦', '6', '♠']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1]


def test_ace_low_straight():
    """Testing Ace Low Straight."""
    hand_amount = 3
    hands_array = ['A', '♣', '2', '♣', '9', '♠', '5', '♦', '2', '♠', 'J', '♦']
    ftr = ['3', '♦', '4', '♦', '5', '♥', 'K', '♦', '8', '♠']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1]


def test_ace_low_straight_on_board():
    """Testing ace low straight on the board - full split pot."""
    hand_amount = 4
    hands_array = ['7', '♣', '8', '♣', '9', '♠', 'T', '♦', 'J', '♠', 'Q', '♦', 'A', '♥', 'A', '♠']
    ftr = ['A', '♦', '2', '♦', '3', '♥', '4', '♠', '5', '♠']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1, 2, 3, 4]


def test_ace_low_straight_on_board_two_sixes():
    """Testing ace low straight on the board - but two hands have a six."""
    hand_amount = 4
    hands_array = ['6', '♣', '8', '♣', '9', '♠', 'T', '♦', 'J', '♠', 'Q', '♦', 'A', '♥', '6', '♠']
    ftr = ['A', '♦', '2', '♦', '3', '♥', '4', '♠', '5', '♠']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1, 4]


# --- Strength 6 Tests: Flush ---


def test_flush_single_winner():
    """Testing an ace high flush winner."""
    hand_amount = 3
    hands_array = ['J', '♦', 'A', '♦', '4', '♠', '5', '♦', 'K', '♦', '7', '♦']
    ftr = ['T', '♦', 'Q', '♦', '4', '♥', '4', '♦', '6', '♠']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1]


def test_flush_winner_fifth_card():
    """Testing a flush win because of the 5th flush card."""
    hand_amount = 3
    hands_array = ['2', '♦', '6', '♦', '2', '♥', '5', '♥', '3', '♥', '7', '♦']
    ftr = ['K', '♦', 'Q', '♦', '4', '♥', '8', '♦', '9', '♦']
    assert main.testing_function(hand_amount, hands_array, ftr) == [3]


def test_flush_split_pot():
    """Testing a split pot for a flush - against a straight also."""
    hand_amount = 3
    hands_array = ['T', '♥', 'J', '♥', '2', '♥', '5', '♥', '3', '♥', '7', '♥']
    ftr = ['K', '♦', 'Q', '♦', '7', '♦', '8', '♦', '9', '♦']
    assert main.testing_function(hand_amount, hands_array, ftr) == [1, 2, 3]


# --- Strength 7 Tests: Full House ---


# --- Strength 8 Tests: Four Of A Kind ---


# --- Strength 9 Tests: Straight Flush ---


def test_straight_flush():
    """Testing a straight flush."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', '9', '♦', '5', '♦', '2', '♠', 'J', '♦']
    ftr = ['6', '♦', '7', '♥', '7', '♦', 'K', '♦', '8', '♦']
    assert main.testing_function(hand_amount, hands_array, ftr) == [2]


# --- Strength 10 Tests: Royal Flush ---


def test_royal_flush_against_straight_flush():
    """Testing a royal flush against a straight flush."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', 'K', '♦', 'A', '♦', '8', '♦', '9', '♦']
    ftr = ['6', '♣', '7', '♥', 'T', '♦', 'J', '♦', 'Q', '♦']
    assert main.testing_function(hand_amount, hands_array, ftr) == [2]
