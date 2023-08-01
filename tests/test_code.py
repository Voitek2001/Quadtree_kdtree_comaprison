import time
import timeit
import pandas as pd
import os.path

from config import (get_find_argument, generate_testing_set, get_generator_function_arguments, 
    DATA_FILE_NAMES, CSV_DATA_DIR, TEST_UNIT_REPEATS, SQUARE_SIZE, TEST_TIMES_FILE_NAME, 
    STRUCTURE_INITS, STRUCTURE_TYPES, TEST_GENERATOR_FUNCTION_ARGUMENTS)
from generators.points_generator import get_random_point
from helper_classes.json_wrapper import * 


def __run_tests(easy, with_repeats):
    if with_repeats:
        test_repeats = TEST_UNIT_REPEATS
    else:
        test_repeats = 1
    
    times = []
    test_args = get_generator_function_arguments(easy)
    for test_type_i, test_type_args in enumerate(test_args):
        test_times = []
        for arg_i in range(len(test_type_args)):
            build_times_sum, add_times_sum, find_times_sum = ({struct_type: 0 for struct_type in STRUCTURE_TYPES} for _ in range(3))
            for _ in range(test_repeats):
                test_points = generate_testing_set(easy, test_type_i, arg_i)
                find_axis_ranges = get_find_argument(test_type_i)
                add_point = get_random_point(SQUARE_SIZE)
                for struct_type in STRUCTURE_TYPES:
                    start_time = time.time()
                    struct = STRUCTURE_INITS[struct_type](test_points)
                    build_times_sum[struct_type] += time.time() - start_time
                    add_times_sum[struct_type] += timeit.timeit(lambda: struct.find(*find_axis_ranges), number=1)
                    find_times_sum[struct_type] += timeit.timeit(lambda: struct.add(add_point), number=1)

            test_time_res = { 
                struct_type : {
                    'build' : [],
                    'add' : [],
                    'find' : []
                } for struct_type in STRUCTURE_TYPES}
            for struct_type in STRUCTURE_TYPES:
                test_time_res[struct_type]['build'] = build_times_sum[struct_type] / test_repeats
                test_time_res[struct_type]['add'] = add_times_sum[struct_type] / test_repeats
                test_time_res[struct_type]['find'] = find_times_sum[struct_type] / test_repeats
            test_times.append(test_time_res)
        times.append(test_times)

    return times


def __dump_times_as_csv(times):
    column_names = [
        'Liczba punktów',
        'Czas tworzenia KDtree [s]',
        'Czas dodawania punktu KDtree [s]',
        'Czas przeszukiwania KDtree [s]',
        'Czas tworzenia Quadtree [s]',
        'Czas dodawania punktu Quadtree [s]',
        'Czas przeszukiwania Quadtree [s]'
    ]
    for test_type_i, test_type_args in enumerate(TEST_GENERATOR_FUNCTION_ARGUMENTS):
        file_name = os.path.join(CSV_DATA_DIR, DATA_FILE_NAMES[test_type_i] + '.csv')
        csv_data = [[args[0]] for args in test_type_args]
        test_type_times = times[test_type_i]
        for test_i in range(len(test_type_times)):
            csv_data[test_i].extend([
                test_type_times[test_i]['kd_tree']['build'],
                test_type_times[test_i]['kd_tree']['add'],
                test_type_times[test_i]['kd_tree']['find'],
                test_type_times[test_i]['quad_tree']['build'],
                test_type_times[test_i]['quad_tree']['add'],
                test_type_times[test_i]['quad_tree']['find'],
            ])
        df = pd.DataFrame(data = csv_data, columns=column_names)
        df.to_csv(file_name)
    
    
def run_and_dump_tests(easy = False, with_repeats = True, as_csv = True, as_json = True):
    times = __run_tests(easy, with_repeats)
    
    if as_json:
        dump_as_json(
            times, 
            TEST_TIMES_FILE_NAME
        )

    if as_csv: 
        __dump_times_as_csv(times)
