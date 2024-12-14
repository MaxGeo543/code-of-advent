import os

DIRECTORY = os.path.dirname(__file__)

PART_1_TESTS = [
    (os.path.join(DIRECTORY, "test_input.txt"), 374)
]

PART_2_TESTS = [
    (os.path.join(DIRECTORY, "test_input.txt"), (1030, 10)),
    (os.path.join(DIRECTORY, "test_input.txt"), (8410, 100))
]
