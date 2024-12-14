import re

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # parse puzzle input
    LR_instructions = re.sub("\n", "", puzzle_input[0].strip())

    graph = {}
    for line in puzzle_input[2:]:
        line = re.sub(" ", "", line)
        key, val = line.split("=")
        val = re.sub(r"[()\n]", "", val).split(",")
        val = (val[0], val[1])
        graph[key] = val

    steps = 0
    cur_node = "AAA"
    while True:
        if cur_node == "ZZZ":
            break

        dir_idx = steps % len(LR_instructions)
        direction = LR_instructions[dir_idx]
        if direction == "L":
            cur_node = graph[cur_node][0]
        if direction == "R":
            cur_node = graph[cur_node][1]
        # print(cur_node, steps)
        steps += 1

    result = steps

    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # parse puzzle input
    LR_instructions = re.sub("\n", "", puzzle_input[0].strip())

    graph = {}
    for line in puzzle_input[2:]:
        line = re.sub(" ", "", line)
        key, val = line.split("=")
        val = re.sub(r"[()\n]", "", val).split(",")
        val = (val[0], val[1])
        graph[key] = val

    steps = 0
    cycles = []
    cur_nodes = [key for key in graph.keys() if key.endswith("A")]
    for node in cur_nodes:
        # get offset
        steps = 0
        dir_idx = 0
        while node[-1] != "Z":
            # print(node)
            direction = 0 if LR_instructions[dir_idx] == "L" else 1
            node = graph[node][direction]
            steps += 1
            dir_idx = steps % len(LR_instructions)
        cycle = [steps, -steps, []]
        state = (node[-1], dir_idx)
        # does a single step
        direction = 0 if LR_instructions[dir_idx] == "L" else 1
        node = graph[node][direction]
        steps += 1
        dir_idx = steps % len(LR_instructions)

        # get cycle length
        while (node[-1], dir_idx) != state:
            if node[-1] == "Z":
                cycle[2].append(cycle[1] + steps)

            direction = 0 if LR_instructions[dir_idx] == "L" else 1
            node = graph[node][direction]
            steps += 1
            dir_idx = steps % len(LR_instructions)
        cycle[1] += steps

        print(cycle)
        cycles.append(cycle)
    print(cycles)

    result = cycles_hit_at(cycles)

    return result

# list of cycles where a cycle is a tplue with
# 1. cycle offset
# 2. cycle length
# 3. end indeces in cycle
def cycles_hit_at(cycles):
    for i in range(100000000, 1000000000000):
        val = cycles[0][0] + cycles[0][1]*i
        print(val)
        if all([any([(val-cycle[0]) % cycle[1] == end for end in cycle[2]]) for cycle in cycles[1:]]):
            return val
        else:
            continue