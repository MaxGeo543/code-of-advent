def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # preprocess
    puzzle_input = puzzle_input[0].strip()
    puzzle_input = puzzle_input.split(",")
    puzzle_input = [t.split("-") for t in puzzle_input]

    # calculate result
    result = 0
    for (n_min, n_max) in puzzle_input:
        for n in range(int(n_min), int(n_max)+1):

            sn = str(n)
            if len(sn)%2 != 0: continue
            if sn == sn[:len(sn)//2]*2:
                result += n

            
         
    # return result
    return result

def part2(input_file, debug=False):
    from math import ceil
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # preprocess
    puzzle_input = puzzle_input[0].strip()
    puzzle_input = puzzle_input.split(",")
    puzzle_input = [t.split("-") for t in puzzle_input]


    # calculate result
    result = 0
    for (n_min, n_max) in puzzle_input:
        for n in range(int(n_min), int(n_max)+1):
            sn = str(n)
            
            if len(sn) == 1: continue

            lsn = len(sn)
            for l in range(1, ceil(lsn/2)+1):
                if lsn%l != 0: 
                    continue

                if sn == sn[:l]*(lsn//l):
                    result += n
                    break
    
    # return result
    return result

'''
The above is my original solution to part 2.
ChatGPT then made me aware of this property to check if something is a periodic string:

def is_repetition(s: str) -> bool:
    len(sn) > 1 and sn in (sn + sn)[1:-1]

^^^^ this is pretty cool
'''