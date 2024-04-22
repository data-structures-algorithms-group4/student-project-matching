# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# test_algorithm.py
#   Usage in terminal/PyCharm: pytest test_algorithm.py

import pytest
from tests.testing_environment import run_and_check_test_data

##############
# Unit Tests #
##############

def test_td_1(students_filename = 'td_1_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    ''' Run and check test case: test data set 1.
        Expected result: PASS '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed

#@pytest.mark.skip()
def test_td_2(students_filename = 'td_2_students.xlsx', projects_filename = 'td_2_projects.xlsx'):
    ''' Run and check test case: test data set 2.
        Expected result: PASS '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed
