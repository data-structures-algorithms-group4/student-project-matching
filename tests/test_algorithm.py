# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# test_algorithm.py
#   Usage in terminal/PyCharm: pytest test_algorithm.py

import pandas as pd
import pytest
from student_project_matching.matching_algorithm import matching_algorithm
from tests.stable_match_checker import stable_match_checker

TEST_DATA_DIR = '../test_data/'

##########################
# Test Environment Setup #
##########################

# TODO merge with the df reading in app.py
def files_to_df(students_file: str, projects_file: str):
    ''' Converts input files to Pandas DataFrames. '''
    # Load the student and project data from Excel files [app.py]
    # TO-DO: handle txt, csv, etc. formats
    students_df = pd.read_excel(students_file)
    projects_df = pd.read_excel(projects_file)
    return students_df, projects_df

def inject_errors(matches: dict, match_errors: dict):
    ''' Injects errors into matches to check that failing modes do fail stable_match_checker. '''
    for s_error, p_error in match_errors.items():
        matches[s_error] = p_error
    return matches

def run_and_check_test_data(students_file: str, projects_file: str, match_errors: dict = {}) -> (bool, str):
    ''' "Test engine" that BOTH runs and checks algorithm given input files.
        Parameters:
            students_file (str): filename for students' project preference list
            projects_file (str): filename for projects' student preference list
        Optional parameters:
            match_errors (dict): inject errors into matches to test failing modes
        Returns:
            Tuple:
                bool: True or False result of a valid stable match, for unit test assert statement
                str: Informative message about result
    '''

    # Input files processing [app.py]
    # TO-DO: add column names if missing (.txt)
    # TO-DO: convert 'max_students' to numeric if needed
    students_file = TEST_DATA_DIR + students_file
    projects_file = TEST_DATA_DIR + projects_file
    students_df, projects_df = files_to_df(students_file, projects_file)

    # Run algorithm
    matches = matching_algorithm(students_df, projects_df)

    # Inject errors to test failing modes (none by default)
    matches = inject_errors(matches, match_errors)

    # Check algorithm (returns bool, string)
    return stable_match_checker(students_df, projects_df, matches)

##############
# Unit Tests #
##############

#@pytest.mark.skip()
def test_td_1(students_file = 'td_1_students.xlsx', projects_file = 'td_1_projects.xlsx'):
    ''' Run and check test case: test data set 1'''
    result, message = run_and_check_test_data(students_file, projects_file)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed

#@pytest.mark.skip()
def test_td_2(students_file = 'td_2_students.xlsx', projects_file = 'td_2_projects.xlsx'):
    ''' Run and check test case: test data set 2'''
    result, message = run_and_check_test_data(students_file, projects_file)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed

@pytest.mark.skip()
def test_td_2_inject_errors(students_file = 'td_2_students.xlsx', projects_file = 'td_2_projects.xlsx'):
    ''' Run and check test case: test data set 2'''
    match_errors = {'s8': 'p1', 's5': 'p3'} # UNSTABLE pair
    #match_errors = {'s8': 'p4'}  # INVALID: P not in Sp
    #match_errors = {'s8': 'p2'}  # INVALID: S not in Pp
    #match_errors = {'s9': 'p1'} # INVALID: Pmax violated
    #match_errors = {}
    result, message = run_and_check_test_data(students_file, projects_file, match_errors)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed
