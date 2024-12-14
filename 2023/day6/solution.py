import re
import math

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # parsing the ouzzle input
    times = [re.sub("\n", "", num) for num in puzzle_input[0].split(":")[1].split(" ") if num != ""]
    distances = [re.sub("\n", "", num) for num in puzzle_input[1].split(":")[1].split(" ") if num != ""]

    races = [(int(times[i]), int(distances[i])) for i in range(len(times))]

    result = 1

    # calculation (I spent more time writing this comment than implementing it lol)
    # let x = length button held
    # -> time left after holding button is (time-x)
    # speed is same as length button held, so x
    # distance traveled = x*(time-x) = x*time - x**2 = f(x)
    # we want to know the number of (whole) x such that f(x) > distance
    # we could try for each value of x but there should be a better solution
    # we want to know f(x) - distance > 0
    # f(x) is a quadratic polynomial with negative leading coefficient
    # therefore it has a maximum and should have 2 roots
    # if we calculate the roots, all numbers between the roots are valid values for x
    # we can calculate roots using the (simplified) quadratic formula (pq-formula)
    # x_{1,2} = -\frac{p}{2} +- \sqrt{\frac{p^2}{4} - q}
    # to get p and q, we normalize the function by multiplying by -1:
    # (- x**2 + time*x - distance) * (-1) = x**2 - time*x + distance
    # p = -time, q = distance
    for race in races:
        # assigning p and q
        time = race[0]
        distance = race[1]

        p = -time
        q = distance

        # using pq-formula to get roots
        root1 = -p / 2 - math.sqrt(p ** 2 / 4 - q)
        root2 = -p / 2 + math.sqrt(p ** 2 / 4 - q)

        # get integers between roots
        num = math.ceil(root2) - math.floor(root1) - 1
        result *= num

    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # parsing the ouzzle input
    time = int(re.sub(" ", "", re.sub("\n", "", puzzle_input[0].split(":")[1])))
    distance = int(re.sub(" ", "", re.sub("\n", "", puzzle_input[1].split(":")[1])))

    # assigning p and q
    p = -time
    q = distance

    # using pq-formula to get roots
    root1 = -p / 2 - math.sqrt(p ** 2 / 4 - q)
    root2 = -p / 2 + math.sqrt(p ** 2 / 4 - q)

    # get integers between roots
    result = math.ceil(root2) - math.floor(root1) - 1

    return result
