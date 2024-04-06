# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# test_input_validation.py
#   Usage in terminal/PyCharm: pytest test_input_validation.py

import pytest
from tests.testing_environment import run_and_check_test_data

##############
# Unit Tests #
##############

def test_double_names_students(students_filename = 'double_names_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    ''' Run and check test case: duplicated student name in student file.
        Expected result: FAIL '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed

def test_double_names_projects(students_filename = 'td_1_students.xlsx', projects_filename = 'double_names_projects.xlsx'):
    ''' Run and check test case: duplicated project name in project file.
        Expected result: FAIL '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed

def test_false_project_name(students_filename = 'false_p_name_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    ''' Run and check test case: duplicated project name in project file.
        Expected result: FAIL '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed
