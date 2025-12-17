import os

DIRECTORY = os.path.dirname(__file__)

PART_1_TESTS = [
    (os.path.join(DIRECTORY, "test_input.txt"), 3)
]

PART_2_TESTS = [
    (os.path.join(DIRECTORY, "test_input.txt"), 6),

    (os.path.join(DIRECTORY, "test_input2.txt"), 1),
    (os.path.join(DIRECTORY, "test_input3.txt"), (1, 1))
]
