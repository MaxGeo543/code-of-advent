'''
--- Day 8: Haunted Wasteland ---

You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

--- Part Two ---

The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the instructions, but you've barely left your starting position. It's going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?

'''

import re

# get paths of input files
from pathlib import Path
mod_path = Path(__file__).parent
PUZZLE_INPUT_PATH = Path(mod_path, "puzzle_input.txt")
TEST_INPUT_PATH = Path(mod_path, "test_input.txt")
TEST_INPUT_2_PATH = Path(mod_path, "test_input_2.txt")

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
        val = re.sub("[\(\)\n]", "", val).split(",")
        val = (val[0], val[1])
        graph[key] = val
    
    steps = 0
    cur_node = "AAA"
    while True:
        if cur_node == "ZZZ":
            break

        dir_idx = steps%len(LR_instructions)
        direction = LR_instructions[dir_idx]
        if direction == "L":
            cur_node = graph[cur_node][0]
        if direction == "R":
            cur_node = graph[cur_node][1]
        # print(cur_node, steps)
        steps += 1
    
    result = steps
        
    print(result)
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
        val = re.sub("[\(\)\n]", "", val).split(",")
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
            dir_idx = steps%len(LR_instructions)
        cycle = [steps, -steps, []]
        state = (node[-1], dir_idx)
        # does a single step
        direction = 0 if LR_instructions[dir_idx] == "L" else 1
        node = graph[node][direction]
        steps += 1
        dir_idx = steps%len(LR_instructions)

        # get cycle length
        while (node[-1], dir_idx) != state:
            if node[-1] == "Z":
                cycle[2].append(cycle[1]+steps)

            direction = 0 if LR_instructions[dir_idx] == "L" else 1
            node = graph[node][direction]
            steps += 1
            dir_idx = steps%len(LR_instructions)
        cycle[1] += steps

        print(cycle)
        cycles.append(cycle)
    print(cycles)

    
    result = cycles_hit_at(cycles)
        
    print(result)
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


if __name__ == "__main__":
    assert part1(TEST_INPUT_PATH) == 2
    # assert part2(TEST_INPUT_2_PATH) == 6
    
    # part1(PUZZLE_INPUT_PATH) # returned 16579
    # print(cycles_hit_at([(1,49), (4,25), (31,33)]))
    print(1)
    part2(PUZZLE_INPUT_PATH)