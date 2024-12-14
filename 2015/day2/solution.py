def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()



    # calculate result
    result = 0
    for line in puzzle_input:
        # first we parse the line into a list of its dimensions
        dimensions = [int(d) for d in line.split("x")]
        dim = range(len(dimensions))
        # then we iterate over the dimensions twice to get the area of all surfaces as a list
        areas = [dimensions[i]*dimensions[j] for i in dim for j in range(i+1, len(dim))]
        # then we can just add twice the sum of the areas and the minimum to the result
        result += 2*sum(areas) + min(areas)
    
    # return result
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

        # calculate result
        result = 0
        for line in puzzle_input:
            # first we parse the line into a list of its dimensions
            dimensions = [int(d) for d in line.split("x")]
            result += dimensions[0]*dimensions[1]*dimensions[2]

            # get the smallest side
            first = min(dimensions)
            dimensions.remove(first)

            # get the second-smallest side
            second = min(dimensions)

            # then we can just add twice the sum of the areas and the minimum to the result
            result += 2 * (first + second)
    
    # return result
    return result
