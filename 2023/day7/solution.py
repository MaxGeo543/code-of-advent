# hands:
# five of a kind   len(cards) * 7
# four of a kind                6
# full house                    5
# three of a kind               4
# two pair                      3
# one pair                      2
# high card                     1
def rank_hand(hand):
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    hand_score = 1
    # determine hand score
    if all(c == hand[0] for c in hand):  # five of a kind
        hand_score = 7
    elif any(hand.count(c) == 4 for c in hand):  # four of a kind
        hand_score = 6
    elif any(hand.count(c) == 3 for c in hand) and any(hand.count(c) == 2 for c in hand):  # full house
        hand_score = 5
    elif any(hand.count(c) == 3 for c in hand):  # three of a kind
        hand_score = 4
    elif [hand.count(c) for c in hand].count(2) == 4:  # two pair
        hand_score = 3
    elif any(hand.count(c) == 2 for c in hand):  # one pair
        hand_score = 2
    else:  # high card
        hand_score = 1

    total_score = 0
    # treating hands as numbers base 13
    hand_size = len(hand)
    for i in range(hand_size):
        total_score += cards.index(hand[hand_size - i - 1]) * 13 ** i
    # most significant digit will be the hand score
    total_score += hand_score * 13 ** hand_size

    return total_score


def rank_hand_jokers(hand):
    cards = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

    hand_score = 1
    # determine hand score
    if hand.count("J") == 5 or any(c != "J" and hand.count(c) + hand.count("J") == 5 for c in hand):  # five of a kind
        hand_score = 7
    elif any(c != "J" and hand.count(c) + hand.count("J") == 4 for c in hand):  # four of a kind
        hand_score = 6
    elif (hand.count("J") == 2 and any(c != "J" and hand.count(c) == 2 for c in hand)) or (
            hand.count("J") == 1 and [hand.count(c) for c in hand].count(2) == 4) or (
            any(hand.count(c) == 2 for c in hand) and any(hand.count(c) == 3 for c in hand)):  # full house
        hand_score = 5
    elif any(c != "J" and hand.count(c) + hand.count("J") == 3 for c in hand):  # three of a kind
        hand_score = 4
    elif [hand.count(c) for c in hand].count(2) == 4:  # two pair
        hand_score = 3
    elif any(c != "J" and hand.count(c) + hand.count("J") == 2 for c in hand):  # one pair
        hand_score = 2
    else:  # high card
        hand_score = 1

    total_score = 0
    # treating hands as numbers base 13
    hand_size = len(hand)
    for i in range(hand_size):
        total_score += cards.index(hand[hand_size - i - 1]) * 13 ** i
    # most significant digit will be the hand score
    total_score += hand_score * 13 ** hand_size

    return total_score

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    hands_bids = []
    # parse puzzle input
    for line in puzzle_input:
        h_b = line.split(" ")
        hands_bids.append((h_b[0], int(h_b[1])))

    # sort hands
    hands_bids.sort(key=lambda x: rank_hand(x[0]))

    # add up result
    result = 0
    for i in range(len(hands_bids)):
        result += (i + 1) * hands_bids[i][1]

    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    hands_bids = []
    # parse puzzle input
    for line in puzzle_input:
        h_b = line.split(" ")
        hands_bids.append((h_b[0], int(h_b[1])))

    # sort hands
    hands_bids.sort(key=lambda x: rank_hand_jokers(x[0]))

    # add up result
    result = 0
    for i in range(len(hands_bids)):
        result += (i + 1) * hands_bids[i][1]

    return result