import threading
import pytest

# define a list of test modules
test_modules = ["D:\\Project\\BookStore\\BookStoreApp\\tests\\book\\test_views\\test_home_page.py"]


# define a function to run tests in a given module
def run_tests(module):
    pytest.main(args=[module, "-q"])


# create a list of threads, one for each module
threads = [threading.Thread(target=run_tests, args=[module]) for module in test_modules]

# start all threads
for thread in threads:
    thread.start()

# wait for all threads to finish before continuing
for thread in threads:
    thread.join()

# all tests have finished
print("All tests completed")
