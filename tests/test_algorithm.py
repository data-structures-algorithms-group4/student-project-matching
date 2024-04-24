# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# test_algorithm.py
#   Usage in terminal/PyCharm: pytest test_algorithm.py

import pytest
from tests.testing_environment import run_and_check_test_data, config_logging

##############
# Unit Tests #
##############
# def config_logging(log_filename: str, log_level_str: str)
# log_level_str options: 'DEBUG', 'INFO' (default), 'WARNING', 'ERROR', 'CRITICAL'

#@pytest.mark.skip()
def test_td_1(students_filename = 'td_1_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    ''' Test data set 1. Expect: PASS'''
    config_logging('test_td_1.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_td_2(students_filename = 'td_2_students.xlsx', projects_filename = 'td_2_projects.xlsx'):
    ''' Test data set 2. Expect: PASS'''
    config_logging('test_td_2.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_s_not_chosen(students_filename = 'td_1_students.xlsx', projects_filename = 'p_td_1_displaced_s_not_chosen.xlsx'):
    ''' One student not chosen by any projects (after reeval). Expect: PASS'''
    config_logging('test_s_not_chosen.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_p_not_chosen(students_filename = 's_project_not_chosen.xlsx', projects_filename = 'p_project_not_chosen.xlsx'):
    ''' One project not chosen by any students. Expect: PASS'''
    config_logging('test_p_not_chosen.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_s_lose_reeval(students_filename = 's_project_pref_ties.xlsx', projects_filename = 'p_student_pref_ties_lose_reeval.xlsx'):
    ''' Test reevaluation case where student does not "win" a spot. Expect: PASS'''
    config_logging('test_s_lose_reeval.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

@pytest.mark.skip()
def test_s_vary_p_pref_size(students_filename = 's_varying_preferences_to_projects.xlsx', projects_filename = 'p_varying_preferences_to_projects.xlsx'):
    ''' Vary size of S preference list of Ps. Expect: PASS'''
    config_logging('test_s_vary_p_pref_size.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message
