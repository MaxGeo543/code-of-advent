import os

DIRECTORY = os.path.dirname(__file__)

PART_1_TESTS = [
    (os.path.join(DIRECTORY, "test_input_1.txt"), 2),
    (os.path.join(DIRECTORY, "test_input_2.txt"), 4),
    (os.path.join(DIRECTORY, "test_input_3.txt"), 2)
]

PART_2_TESTS = [
    (os.path.join(DIRECTORY, "test_input_2.txt"), 3),
    (os.path.join(DIRECTORY, "test_input_3.txt"), 11),
    (os.path.join(DIRECTORY, "test_input_4.txt"), 3),
]
