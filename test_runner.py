from tests.test_code import run_and_dump_tests
from config import generate_testing_data

# generate_testing_data(easy=False)
run_and_dump_tests(easy=False, with_repeats=True, as_csv=True)