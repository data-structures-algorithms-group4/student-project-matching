# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# test_checker.py
#   Usage in terminal/PyCharm: pytest test_checker.py

import pytest
from tests.testing_environment import run_and_check_test_data

####################
# Validate Checker #
####################

#@pytest.mark.skip()
def test_td_2_inject_errors(students_filename = 'td_2_students.xlsx', projects_filename = 'td_2_projects.xlsx'):
    ''' Run and check test case: test data set 2'''
    match_errors = {'s8': 'p1', 's5': 'p3'} # UNSTABLE pair
    #match_errors = {'s8': 'p4'}  # INVALID: P not in Sp
    #match_errors = {'s8': 'p2'}  # INVALID: S not in Pp
    #match_errors = {'s9': 'p1'} # INVALID: Pmax violated
    #match_errors = {}
    result, message = run_and_check_test_data(students_filename, projects_filename, match_errors)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed
