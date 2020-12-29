import main as main
import pytest

# Commands to run
# python3 -m pytest tests.py
# coverage run -m pytest tests.py
# coverage report
# coverage html -> To open the report, type 'explorer.exe engine_py.html' (will open locally)

# ♦ ♥ ♠ ♣

'''
main.testing_function(hand_amount, hands_array, ftr) returns:
- result[0]: The winning hands in a list: For example, [1, 3] represents a split pot between
hands 1 and 3, and [2] represents a won hand for hand 2
- result[1]: The strengths of each hand in a list: For example, [5, 6, 7] represents a Straight,
Flush and a Full House from hands 1, 2, and 3 respectively

Copy and paste tempelate
result = main.testing_function(hand_amount, hands_array, ftr)
assert result[0] == []
assert result[1] == []
'''

# --- Strength 1 Tests: High Card ---


def test_high_card_win():
    """Testing high card win."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', '9', '♠', '5', '♦', '2', '♠', 'J', '♦']
    ftr = ['3', '♦', 'T', '♦', '7', '♥', 'K', '♦', '8', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [3]
    assert result[1] == [1, 1, 1]


def test_high_card_split_pot():
    """Testing high card split pot."""
    hand_amount = 3
    hands_array = ['4', '♣', 'J', '♣', '9', '♠', '5', '♦', '2', '♠', 'J', '♦']
    ftr = ['3', '♦', 'T', '♦', '7', '♥', 'K', '♦', '8', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 3]
    assert result[1] == [1, 1, 1]


def test_high_cards_on_board():
    """Testing the board containing all five high cards."""
    hand_amount = 2
    hands_array = ['4', '♣', '2', '♣', '6', '♠', '5', '♠']
    ftr = ['K', '♦', 'Q', '♦', 'J', '♦', '8', '♦', 'A', '♥']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2]
    assert result[1] == [1, 1]


# --- Strength 2 Tests: Pair ---


def test_pocket_aces():
    """Testing a simple pocket aces win."""
    hand_amount = 3
    hands_array = ['A', '♣', 'A', '♠', '3', '♥', '5', '♠', '6', '♥', 'T', '♥']
    ftr = ['K', '♦', 'Q', '♦', 'J', '♦', '8', '♦', '7', '♥']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [2, 1, 1]


def test_pair_on_board_high_card():
    """Testing pair on the board with a high card win."""
    hand_amount = 3
    hands_array = ['4', '♣', '5', '♥', '3', '♥', '5', '♠', '6', '♥', 'T', '♥']
    ftr = ['K', '♦', 'K', '♣', 'J', '♦', '8', '♦', '7', '♥']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [3]
    assert result[1] == [2, 2, 2]


def test_split_pair():
    """Testing two pocket pairs split pot."""
    hand_amount = 2
    hands_array = ['4', '♣', '4', '♥', '4', '♦', '4', '♠']
    ftr = ['K', '♦', '2', '♣', 'J', '♦', '8', '♦', '7', '♥']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2]
    assert result[1] == [2, 2]


# --- Strength 3 Tests: Two Pair ---


def test_won_two_pair():
    """Testing a won two pair hand."""
    hand_amount = 3
    hands_array = ['3', '♣', '4', '♥', '6', '♦', '7', '♠', '8', '♠', '9', '♠']
    ftr = ['Q', '♦', '8', '♣', '9', '♦', '4', '♦', '3', '♥']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [3]
    assert result[1] == [3, 1, 3]


def test_split_two_pair():
    """Testing a split two pair on the whole board."""
    hand_amount = 3
    hands_array = ['4', '♦', '4', '♥', 'K', '♥', 'Q', '♦', 'J', '♠', 'T', '♠']
    ftr = ['A', '♣', '9', '♥', '5', '♣', '5', '♥', '9', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2, 3]
    assert result[1] == [3, 3, 3]


def test_won_two_pair_using_kicker():
    """Testing a won two pair using a kicker."""
    hand_amount = 3
    hands_array = ['4', '♦', '6', '♥', 'K', '♥', 'Q', '♦', 'J', '♠', 'T', '♠']
    ftr = ['A', '♣', 'A', '♥', '5', '♣', '5', '♥', '9', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [2]
    assert result[1] == [3, 3, 3]


# --- Strength 4 Tests: Three Of A Kind ---


def test_three_of_a_kind():
    """Testing Three Of a Kind win."""
    hand_amount = 3
    hands_array = ['A', '♦', 'A', '♥', 'K', '♦', 'K', '♥', 'Q', '♦', 'Q', '♥']
    ftr = ['A', '♣', '3', '♣', '5', '♠', '7', '♣', '9', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [4, 2, 2]


def test_three_of_a_kind_win_kicker():
    """Testing a three of a kind win from the two kickers."""
    hand_amount = 3
    hands_array = ['9', '♦', 'K', '♥', 'K', '♦', '8', '♥', 'Q', '♦', '6', '♥']
    ftr = ['A', '♣', 'A', '♦', '5', '♠', '7', '♣', 'A', '♥']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [4, 4, 4]


def test_three_of_a_kind_split_pot():
    """Testing a split against two hands for three of a kind."""
    hand_amount = 3
    hands_array = ['9', '♦', 'K', '♥', 'Q', '♠', '8', '♥', 'Q', '♥', '6', '♥']
    ftr = ['Q', '♣', 'Q', '♦', '5', '♠', 'T', '♣', 'A', '♥']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [2, 3]
    assert result[1] == [2, 4, 4]


# --- Strength 5 Tests: Straight ---


def test_split_straight():
    """Testing Split Straight."""
    hand_amount = 3
    hands_array = ['J', '♣', 'Q', '♣', '9', '♠', '5', '♦', '2', '♠', 'J', '♦']
    ftr = ['6', '♦', 'T', '♦', 'Q', '♥', 'K', '♦', 'A', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 3]
    assert result[1] == [5, 1, 5]


def test_straight_against_trips():
    """Testing a royal straight."""
    hand_amount = 3
    hands_array = ['J', '♣', 'Q', '♣', 'T', '♠', '5', '♦', 'A', '♠', 'A', '♣']
    ftr = ['T', '♦', 'K', '♦', '4', '♥', 'A', '♦', '6', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [5, 2, 4]


def test_ace_low_straight():
    """Testing Ace Low Straight."""
    hand_amount = 3
    hands_array = ['A', '♣', '2', '♣', '9', '♠', '5', '♦', '8', '♠', 'K', '♦']
    ftr = ['3', '♦', '4', '♦', '5', '♥', 'K', '♦', '8', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [5, 2, 3]


def test_ace_low_straight_on_board():
    """Testing ace low straight on the board - full split pot."""
    hand_amount = 4
    hands_array = ['7', '♣', '8', '♣', '9', '♠', 'T', '♦', 'J', '♠', 'Q', '♦', 'A', '♥', 'A', '♠']
    ftr = ['A', '♦', '2', '♦', '3', '♥', '4', '♠', '5', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2, 3, 4]
    assert result[1] == [5, 5, 5, 5]


def test_ace_low_straight_on_board_two_sixes():
    """Testing ace low straight on the board - but two hands have a six."""
    hand_amount = 4
    hands_array = ['6', '♣', '8', '♣', '9', '♠', 'T', '♦', 'J', '♠', 'Q', '♦', 'A', '♥', '6', '♠']
    ftr = ['A', '♦', '2', '♦', '3', '♥', '4', '♠', '5', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 4]
    assert result[1] == [5, 5, 5, 5]


# --- Strength 6 Tests: Flush ---


def test_flush_single_winner():
    """Testing an ace high flush winner."""
    hand_amount = 3
    hands_array = ['J', '♦', 'A', '♦', '3', '♠', '3', '♦', 'K', '♦', '7', '♦']
    ftr = ['T', '♦', 'Q', '♦', '4', '♥', '4', '♦', '6', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [6, 3, 6]


def test_flush_winner_fifth_card():
    """Testing a flush win because of the 5th flush card."""
    hand_amount = 3
    hands_array = ['2', '♦', '6', '♦', '6', '♥', '7', '♥', '3', '♥', '7', '♦']
    ftr = ['K', '♦', 'Q', '♦', '5', '♥', '8', '♦', '9', '♦']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [3]
    assert result[1] == [6, 5, 6]


def test_flush_split_pot():
    """Testing a split pot for a flush - against a straight also."""
    hand_amount = 3
    hands_array = ['T', '♥', 'J', '♥', '2', '♥', '5', '♥', '3', '♥', '7', '♥']
    ftr = ['K', '♠', 'Q', '♠', '7', '♠', '8', '♠', '9', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2, 3]
    assert result[1] == [6, 6, 6]


def test_flush_against_other_strengths():
    """Testing a flush win against other strengths."""
    hand_amount = 5
    hands_array = ['Q', '♥', '2', '♠', '5', '♠', '3', '♦', '6', '♣', 'A', '♣', 'T', '♣', 'T', '♦',
                   '7', '♥', '8', '♥']
    ftr = ['T', '♥', 'A', '♥', '6', '♥', '4', '♥', '2', '♦']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [6, 5, 3, 4, 6]


# --- Strength 7 Tests: Full House ---


def test_full_house_win():
    """Testing a full house win."""
    hand_amount = 3
    hands_array = ['T', '♥', 'T', '♦', '2', '♥', '5', '♠', '3', '♠', '7', '♥']
    ftr = ['Q', '♦', 'Q', '♠', '7', '♦', '7', '♠', 'T', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [7, 3, 7]


def test_full_house_win_2():
    """Testing another full house win."""
    hand_amount = 3
    hands_array = ['6', '♥', '6', '♦', '2', '♥', '2', '♠', '3', '♠', '5', '♥']
    ftr = ['K', '♦', 'A', '♠', '7', '♦', '7', '♠', '7', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [7, 7, 4]


def test_full_house_split():
    """Testing a full house split pot amongst two hands."""
    hand_amount = 3
    hands_array = ['Q', '♥', '4', '♦', 'Q', '♣', 'K', '♠', '3', '♠', '3', '♥']
    ftr = ['Q', '♦', 'Q', '♠', '3', '♦', '4', '♥', '4', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2]
    assert result[1] == [7, 7, 7]


def test_full_house_on_board_split():
    """Testing a full house on the board, with a split pot."""
    hand_amount = 3
    hands_array = ['A', '♥', '4', '♥', '7', '♣', '7', '♠', '6', '♠', '6', '♥']
    ftr = ['K', '♦', 'K', '♠', 'K', '♥', '9', '♥', '9', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2, 3]
    assert result[1] == [7, 7, 7]


def test_full_house_on_board_winner():
    """Testing a full house on the board, but there's a winner with a higher pair val."""
    hand_amount = 3
    hands_array = ['A', '♥', '4', '♥', '7', '♣', '7', '♠', 'T', '♠', 'T', '♥']
    ftr = ['K', '♦', 'K', '♠', 'K', '♥', '9', '♥', '9', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [3]
    assert result[1] == [7, 7, 7]


# --- Strength 8 Tests: Four Of A Kind ---


def test_four_of_a_kind_winner():
    """Testing a single four of a kind winner."""
    hand_amount = 3
    hands_array = ['2', '♥', '2', '♣', '7', '♣', '7', '♠', 'T', '♠', 'T', '♥']
    ftr = ['2', '♦', '7', '♦', 'T', '♦', '9', '♣', '2', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [8, 7, 7]


def test_four_of_a_kind_2():
    """Testing a four of a kind, where three of the cards are on the board."""
    hand_amount = 3
    hands_array = ['2', '♥', '7', '♣', '6', '♣', '8', '♠', 'T', '♠', 'J', '♥']
    ftr = ['2', '♦', '7', '♦', 'Q', '♦', '2', '♣', '2', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [8, 4, 4]


def test_four_of_a_kind_stronger():
    """Testing one four of a kind beating another."""
    hand_amount = 4
    hands_array = ['8', '♥', '8', '♣', '7', '♣', '7', '♠', 'K', '♠', 'K', '♥', '3', '♣', '4', '♣']
    ftr = ['8', '♦', '7', '♦', 'K', '♦', 'K', '♣', '8', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [3]
    assert result[1] == [8, 7, 8, 3]


def test_four_of_a_kind_split():
    """Testing a split pot, four of a kind."""
    hand_amount = 3
    hands_array = ['A', '♥', '5', '♣', '9', '♣', '9', '♠', 'A', '♠', 'A', '♣']
    ftr = ['8', '♦', '8', '♦', '8', '♦', '9', '♦', '8', '♠']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 3]
    assert result[1] == [8, 8, 8]


def test_four_of_a_kind_three_on_board():
    """Testing a four of a kind, where three of a kind is on the board."""
    hand_amount = 2
    hands_array = ['A', '♥', '5', '♣', '9', '♣', '9', '♦']
    ftr = ['A', '♦', 'A', '♠', '3', '♦', '4', '♦', 'A', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1]
    assert result[1] == [8, 7]


# --- Strength 9 Tests: Straight Flush ---


def test_straight_flush_win():
    """Testing a straight flush, single winner."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♦', '9', '♦', '5', '♦', '7', '♠', '6', '♥']
    ftr = ['6', '♦', '7', '♥', '7', '♦', 'K', '♦', '8', '♦']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [2]
    assert result[1] == [6, 9, 7]


def test_straight_flush_split():
    """Testing a split between all hands for a straight flush."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', '8', '♦', '5', '♦', '2', '♠', '4', '♦']
    ftr = ['K', '♦', 'Q', '♦', 'J', '♦', '9', '♦', 'T', '♦']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2, 3]
    assert result[1] == [9, 9, 9]


def test_straight_flush_overcard_winner():
    """Testing a straight flush win, higher straight value."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', 'K', '♦', '5', '♦', '2', '♠', '8', '♦']
    ftr = ['8', '♠', 'Q', '♦', 'J', '♦', '9', '♦', 'T', '♦']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [2]
    assert result[1] == [5, 9, 9]


def test_straight_flush_ace_low():
    """Testing an ace low straight flush."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', 'K', '♦', '5', '♦', 'A', '♠', 'A', '♥']
    ftr = ['A', '♣', '3', '♣', '5', '♣', 'A', '♦', '2', '♦']
    result = main.testing_function(hand_amount, hands_array, ftr)
    print(result)
    assert result[0] == [1]
    assert result[1] == [9, 3, 8]


# --- Strength 10 Tests: Royal Flush ---


def test_royal_flush_against_straight_flush():
    """Testing a royal flush against a straight flush."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', 'K', '♦', 'A', '♦', '8', '♦', '9', '♦']
    ftr = ['6', '♣', '7', '♥', 'T', '♦', 'J', '♦', 'Q', '♦']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [2]
    assert result[1] == [1, 10, 9]


def test_royal_flush_on_board():
    """Testing a royal flush on the board - split pot - will probably never happen!"""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', 'K', '♦', 'A', '♦', 'Q', '♦', '9', '♦']
    ftr = ['T', '♣', 'J', '♣', 'Q', '♣', 'K', '♣', 'A', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [1, 2, 3]
    assert result[1] == [10, 10, 10]


def test_royal_flush_coverage():
    """A general test for royal flush to gain coverage."""
    hand_amount = 3
    hands_array = ['4', '♣', '2', '♣', '6', '♦', 'Q', '♣', '5', '♦', '9', '♦']
    ftr = ['T', '♣', 'J', '♣', 'Q', '♦', 'K', '♣', 'A', '♣']
    result = main.testing_function(hand_amount, hands_array, ftr)
    assert result[0] == [2]
    assert result[1] == [6, 10, 5]
