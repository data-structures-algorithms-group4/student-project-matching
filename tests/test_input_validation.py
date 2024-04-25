# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# test_input_validation.py
#   Usage in terminal/PyCharm: pytest test_input_validation.py

import pytest
from tests.testing_environment import run_and_check_test_data

##############
# Unit Tests #
##############

#@pytest.mark.skip()
def test_s_duplicated(students_filename = 'double_names_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    ''' Student file: duplicated student name. Expect: PASS (error and message) '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert not result and message == 'Not all students are unique'

#@pytest.mark.skip()
def test_p_duplicated(students_filename = 'td_1_students.xlsx', projects_filename = 'double_names_projects.xlsx'):
    ''' Project file: duplicated project name. Expect: PASS (error and message) '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert not result and message == 'Not all projects are unique'

#@pytest.mark.skip()
def test_s_duplicated_p(students_filename = 'same_preference_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    '''  Student file: duplicated project name in preference list. Expect: PASS (error and message) '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert not result and message == 'Not all preferences within student are unique'

#@pytest.mark.skip()
def test_p_duplicated_s(students_filename = 'td_1_students.xlsx', projects_filename = 'same_preference_projects.xlsx'):
    '''  Project file: duplicated student name in preference list. Expect: PASS (error and message) '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert not result and message == 'Not all preferences within project are unique'

#@pytest.mark.skip()
def test_s_false_p(students_filename = 'false_p_name_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    '''  Student file: incorrect project name in preference list. Expect: PASS (error and message) '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert not result and message == 'Some projects in the student file are not in the projects file'

#@pytest.mark.skip()
def test_p_false_s(students_filename = 'td_1_students.xlsx', projects_filename = 'false_s_projects.xlsx'):
    ''' Project file: incorrect student name in preference list. Expect: PASS (error and message) '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert not result and message == 'Some students in the project file are not in the students file'

#@pytest.mark.skip()
def test_p_zero_max(students_filename = 'td_1_students.xlsx', projects_filename = 'p_zero_max.xlsx'):
    ''' Project file with a maximum capacity of zero. Expect: PASS (error and message) '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert not result and message == 'max_students is not always an integer greater than zero'

# @pytest.mark.skip()
def test_p_wrong_max(students_filename='td_1_students.xlsx', projects_filename='wrong_max_projects.xlsx'):
    '''  Project file: illegal maximum capacities. Expect: PASS (error and message) '''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert not result and message == 'max_students is not always an integer greater than zero'
