import os.path

from generators.points_generator import *
from helper_classes.json_wrapper import *
from quad_tree.quad_tree import quad_tree
from kd_tree.kd_tree import KDTree

EASY_TESTING_DATA_DIR = './tests/points_data/easy'
HARD_TESTING_DATA_DIR = './tests/points_data/hard'
TEST_TIMES_FILE_NAME = './tests/times.json'
CSV_DATA_DIR = './tests/csv'

STRUCTURE_TYPES = ['quad_tree', 'kd_tree']
STRUCTURE_INITS = {
    'quad_tree': quad_tree,
    'kd_tree' : KDTree
}

DATA_FILE_NAME_FORMAT = '{name}_{index}'
TEST_UNIT_REPEATS = 20       # no. repeats for every test to take average time
SQUARE_SIZE = 100

GENERATOR_FUNCTIONS = [
    generate_uniform_points,
    generate_normal_points,
    generate_points_on_grid,
    generate_clustered_points,
    generate_points_on_cross,
    generate_points_on_square_edges
]
    
    
TEST_GENERATOR_FUNCTION_ARGUMENTS = [
    [
        (int(1e3),), (int(1e4),), (int(5e4),), (int(1e5),), 
    ],
    [
        (int(1e3),), (int(1e4),), (int(5e4),), (int(1e5),), 
    ],
    [
        (961,), (9801,), (48400,), (99856,),
    ],
    [
        (int(1e3),), (int(1e4),), (int(5e4),), (int(1e5),), 
    ],
    [
        (int(1e3),), (int(1e4),), (int(5e4),), (int(1e5),), 
    ],
    [
        (int(1e3),), (int(1e4),), (int(5e4),), (int(1e5),), 
    ]
]


EASY_GENERATOR_FUNCTION_ARGUMENTS = [
    [
        (int(1e2),)
    ],
    [
        (int(1e2),)
    ],
    [
        (16, 128)
    ],
    [
        (int(2e2), 100, 3)
    ],
    [
        (int(2e2),)
    ],
    [
        (int(1e2),)
    ]
]


TESTING_FIND_ARGUMENT_RANGES = [
    [
        (0, 100), (0, 100), (0, 100), (0, 100)
    ],
    [
        (37.5, 37.5), (50, 62.5), (37.5, 37.5), (50, 62.5)
    ],
    [
        (0, 100), (0, 100), (0, 100), (0, 100)
    ],
    [
        (0, 100), (0, 100), (0, 100), (0, 100)
    ],
    [
        (25, 25), (55, 75), (25, 25), (55, 75)
    ],
    [
        (0, 0), (0, 100), (0, 0), (0, 100)
    ],
]


DATA_FILE_NAMES = [
    'uniform',
    'normal',
    'grid',
    'clusters',
    'cross',
    'rect'
]


def generate_testing_data(easy = False):
    generator_function_arguments = get_generator_function_arguments(easy)  
    test_data_dir = get_test_data_dir(easy)

    for func_i, func in enumerate(GENERATOR_FUNCTIONS):
        file_name_type = DATA_FILE_NAMES[func_i]
        for i, args in enumerate(generator_function_arguments[func_i]):
            points = func(*args)
            file_name = DATA_FILE_NAME_FORMAT.format(name = file_name_type, index = i)
            dump_as_json(
                points,
                os.path.join(test_data_dir, file_name + '.json')
            )
       
            
def generate_testing_set(easy, func_i, args_i):
    generator_function_arguments = get_generator_function_arguments(easy)  
    args = generator_function_arguments[func_i][args_i]
    func = GENERATOR_FUNCTIONS[func_i]
    points = func(*args)
    return points


def get_test_data(easy = False):
    generator_function_arguments = get_generator_function_arguments(easy) 
    test_data_dir = get_test_data_dir(easy)

    test_data = []
    for func_i in range (len(GENERATOR_FUNCTIONS)):
        file_name_type = DATA_FILE_NAMES[func_i]
        func_data = []
        for i in range(len(generator_function_arguments[func_i])):
            file_name = DATA_FILE_NAME_FORMAT.format(name = file_name_type, index = i)
            func_data.append(
                load_from_json(os.path.join(test_data_dir, file_name + '.json'))
            )
        test_data.append(func_data)
    return test_data


def get_find_argument(test_type_i):
    argument_ranges = TESTING_FIND_ARGUMENT_RANGES[test_type_i]
    arguments = []
    
    for range in argument_ranges:
        if range[0] == range[1]:
            value = range[0]
        else:
            value = random.uniform(*range)
        arguments.append(value)
    
    return [
        min(arguments[0], arguments[1]),
        max(arguments[0], arguments[1]),
        min(arguments[2], arguments[3]),
        max(arguments[2], arguments[3])
    ]


def get_generator_function_arguments(easy):
    if easy:
        return EASY_GENERATOR_FUNCTION_ARGUMENTS
    else:
        return TEST_GENERATOR_FUNCTION_ARGUMENTS 


def get_test_data_dir(easy):
    if easy:
        return EASY_TESTING_DATA_DIR
    else:
        return HARD_TESTING_DATA_DIR 