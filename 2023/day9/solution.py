def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    sequences = []
    # parse puzzle input
    for line in puzzle_input:
        sequences.append([int(s.strip()) for s in line.split(" ")])

    result = 0
    for seq in sequences:
        result += predict_next_value(seq)

    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    sequences = []
    # parse puzzle input
    for line in puzzle_input:
        sequences.append(list(reversed([int(s.strip()) for s in line.split(" ")])))

    result = 0
    for seq in sequences:
        result += predict_next_value(seq)

    return result

def predict_next_value(seq):
    seq_len = len(seq) + 1
    derivatives = [seq]
    while not all(n == 0 for n in derivatives[-1]):
        last_seq = derivatives[-1]
        derivatives.append([last_seq[i] - last_seq[i - 1] for i in range(1, len(last_seq))])

    for der in derivatives:
        der += (seq_len - len(der)) * [0]

    derivatives.reverse()

    for i in range(1, len(derivatives)):
        for j in range(1, seq_len):
            derivatives[i][j] = derivatives[i][j - 1] + derivatives[i - 1][j - 1]
    return derivatives[-1][-1]
