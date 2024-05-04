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

##################
# Basic Complete #
##################

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
def test_td_1_csv(students_filename = 'td_1_students.csv', projects_filename = 'td_1_projects.csv'):
    ''' Test data set 1 with CSV files. Expect: PASS'''
    config_logging('test_td_1_csv.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_td_1_txt(students_filename = 'td_1_students.txt', projects_filename = 'td_1_projects.txt'):
    ''' Test data set 1 with text files. Expect: PASS'''
    config_logging('test_td_1_txt.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

##############
# By Matches #
##############

#@pytest.mark.skip()
def test_s_not_chosen(students_filename = 'td_1_students.xlsx', projects_filename = 'p_td_1_displaced_s_not_chosen.xlsx'):
    ''' One student not chosen by any projects (after reeval). Expect: PASS'''
    config_logging('test_s_not_chosen.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_s_not_listed(students_filename = 'td_1_students.xlsx', projects_filename = 'p_td_1_s_not_listed.xlsx'):
    ''' One student not listed by any projects. Expect: PASS'''
    config_logging('test_s_not_listed.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_p_not_chosen(students_filename = 's_project_not_chosen.xlsx', projects_filename = 'p_project_not_chosen.xlsx'):
    ''' One project not chosen by any students. Expect: PASS'''
    config_logging('test_p_not_chosen.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_s_same_first_choice(students_filename = 's_same_first_choice.xlsx', projects_filename = 'p_same_first_choice.xlsx'):
    ''' Students all have same first choice. Expect: PASS'''
    config_logging('test_s_same_first_choice.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_p_same_first_choice(students_filename = 's2_same_first_choice.xlsx', projects_filename = 'p2_same_first_choice.xlsx'):
    ''' Projects all have same first choice. Expect: PASS'''
    config_logging('test_p_same_first_choice.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_s_same_last_choice(students_filename = 's_same_last_choice.xlsx', projects_filename = 'p_same_last_choice.xlsx'):
    ''' Students all have same last choice. Expect: PASS'''
    config_logging('test_s_same_last_choice.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_p_same_last_choice(students_filename = 's2_same_last_choice.xlsx', projects_filename = 'p2_same_last_choice.xlsx'):
    ''' Projects all have same last choice. Expect: PASS'''
    config_logging('test_p_same_last_choice.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_all_pref_ties(students_filename = 's_project_pref_ties.xlsx', projects_filename = 'p_student_pref_ties.xlsx'):
    ''' Both students and projects have all preference ties. Expect: PASS'''
    config_logging('test_all_pref_ties.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_s_lose_reeval(students_filename = 's_project_pref_ties.xlsx', projects_filename = 'p_student_pref_ties_lose_reeval.xlsx'):
    ''' Test reevaluation case where student does not "win" a spot. Expect: PASS'''
    config_logging('test_s_lose_reeval.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#pytest.mark.skip()
def test_no_matches(students_filename = 's_no_matches.xlsx', projects_filename = 'p_no_matches.xlsx'):
    ''' Test case where no students and projects match at all. Expect: PASS'''
    config_logging('test_no_matches.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#############
# By Number #
#############

#@pytest.mark.skip()
def test_p_non_full(students_filename = 'td_1_students.xlsx', projects_filename = 'p_td_1_non_full.xlsx'):
    ''' Projects remain with space after all students matched. Expect: PASS'''
    config_logging('test_p_non_full.log')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

#@pytest.mark.skip()
def test_s_unmatched(students_filename = 'td_1_students.xlsx', projects_filename = 'p_td_1_s_unmatched.xlsx'):
    ''' Some students are unmatched after project spaces have been filled. Expect: PASS'''
    config_logging('test_s_unmatched.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_s_1_blank(students_filename = '1_blank_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    ''' One student has one less project preference than other students. Expect: PASS'''
    config_logging('test_s_1_blank.log', 'DEBUG')
    config_logging('test_s_1_blank.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

#@pytest.mark.skip()
def test_p_1_blank(students_filename = 'td_1_students.xlsx', projects_filename = '1_blank_projects.xlsx'):
    ''' One project has one less student preference than other projects. Expect: PASS'''
    config_logging('test_p_1_blank.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

#@pytest.mark.skip()
def test_s_vary_p_pref_size(students_filename = 's_varying_preferences_to_projects.xlsx', projects_filename = 'p_varying_preferences_to_projects.xlsx'):
    ''' Vary size of student preference list of projects. Expect: PASS'''
    config_logging('test_s_vary_p_pref_size.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

#@pytest.mark.skip()
def test_p_vary_s_pref_size(students_filename = 's2_varying_preferences_to_projects.xlsx', projects_filename = 'p2_varying_preferences_to_projects.xlsx'):
    ''' Vary size of project preference list of students. Expect: PASS'''
    config_logging('test_p_vary_s_pref_size.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

#@pytest.mark.skip()
def test_both_vary_pref_sizes(students_filename = 's_varying_preferences_to_projects.xlsx', projects_filename = 'p2_varying_preferences_to_projects.xlsx'):
    ''' Vary size of both student and project preference lists. Expect: PASS'''
    config_logging('test_both_vary_pref_sizes.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

#@pytest.mark.skip()
def test_s_no_prefs(students_filename = 's_td_1_no_prefs.xlsx', projects_filename = 'td_1_projects.xlsx'):
    ''' Check when a student has an empty project preference list. Expect: PASS'''
    config_logging('test_s_no_prefs.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

#@pytest.mark.skip()
def test_p_no_prefs(students_filename = 'td_1_students.xlsx', projects_filename = 'p_td_1_no_prefs.xlsx'):
    ''' Check when a project has an empty student preference list. Expect: PASS'''
    config_logging('test_p_no_prefs.log', 'DEBUG')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

############
# By P-max #
############

#@pytest.mark.skip()
def test_p_vary_max(students_filename = 'td_1_students.xlsx', projects_filename = 'p_vary_max.xlsx'):
    ''' Projects have varying maximum capacities. Expect: PASS'''
    config_logging('test_p_vary_max.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_p_increased_max(students_filename = 'td_1_students.xlsx', projects_filename = 'p_increased_max.xlsx'):
    ''' Projects have increased maximum capacities greater than its preference list sizes. Expect: PASS'''
    config_logging('test_p_increased_max.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

#@pytest.mark.skip()
def test_p_reduced_max(students_filename = 'td_1_students.xlsx', projects_filename = 'p_reduced_max.xlsx'):
    ''' Projects have reduced maximum capacities less than its preference list sizes. Expect: PASS'''
    config_logging('test_p_reduced_max.log')
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message

###############
# Random Data #
###############

#@pytest.mark.skip()
def test_random_data_n200(students_filename = 'random_student_preferences.csv', projects_filename = 'random_project_assignments.csv'):
    ''' Large size (n=200) random data from test_data_random.ipynb. Expect: PASS'''
    config_logging('test_random_data_n200.log')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

#@pytest.mark.skip()
def test_mds_people(students_filename = 'MDS_students_test.xlsx', projects_filename = 'MDS_projects_test.xlsx'):
    ''' MDS students and fascinating projects for in-class demo. Expect: PASS'''
    config_logging('test_mds_people.log')
    result, message = run_and_check_test_data(students_filename, projects_filename, run_input_val=True)
    assert result, message

