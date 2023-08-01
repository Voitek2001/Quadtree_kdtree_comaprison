from quad_tree.quad_tree import quad_tree
from config import generate_testing_set, get_find_argument
from helper_classes.json_wrapper import dump_as_json, load_from_json

test_index = 0
base_find_argument = (45, 45)
points_path = './tests/presentation/quad_tree'
argument_file_name = 'argument'

get_test_name = lambda find: 'find' if find else 'add'

def run_tests(test_type_index, test_index, find, 
        load_argument_from_file = False, save_argument = False, 
        save_points = False, load_points_from_file = False):
    file_path = points_path + '_' + get_test_name(find) + '.json'
    if load_points_from_file:
        test_data = load_from_json(file_path)
    else:
        test_data = generate_testing_set(True, test_type_index, test_index)

    if save_points:
        dump_as_json(test_data, file_path)
    qt = quad_tree(test_data)
    argument = get_argument(find, load_argument_from_file, save_argument)
    if find:
        qt.visualized_find(*argument)
    else:
        qt.visualized_add(argument)
    

def get_argument(find, from_file, save_argument):
    file_path = points_path + '_' + get_test_name(find) + '_' + argument_file_name + '.json'
    if find:
        if from_file:
            argument = load_from_json(file_path)
        else:
            argument = get_find_argument(test_type_index) 
    else:
        argument = base_find_argument

    if save_argument:
        dump_as_json(argument, file_path)
        
    return argument


test_type_index = 0

# find = True     # find
find = False    # add

run_tests(test_type_index, test_index, find,
    save_points=False, load_points_from_file=True,
    save_argument=False, load_argument_from_file=True)


# run_tests(3, 0, find)