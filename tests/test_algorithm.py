# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# test_algorithm.py
#   Usage in terminal/PyCharm: pytest test_algorithm.py

import pandas as pd
import pytest
from student_project_matching.matching_algorithm import matching_algorithm
from tests.stable_match_checker import stable_match_checker
from student_project_matching.app import parse_df_upload
from werkzeug.datastructures import FileStorage

TEST_DATA_DIR = '../test_data/'

##########################
# Test Environment Setup #
##########################

# TO-DO: Add input validation functions from app.py (PR4, 9)
def validate_inputs(students_df, projects_df):
    ''' Prepare and validate inputs before inputting them to algorithm (from app.py)'''
    students_df = students_df.rename(
        columns={students_df.columns[0]: "student_names"}
    )
    projects_df = projects_df.rename(
        columns={
            projects_df.columns[0]: "project_names",
            projects_df.columns[1]: "max_students",
        }
    )
    projects_df["max_students"] = pd.to_numeric(projects_df["max_students"])
    return students_df, projects_df

def inject_errors(matches: dict, match_errors: dict):
    ''' Injects errors into matches to check that failing modes do fail stable_match_checker. '''
    for s_error, p_error in match_errors.items():
        matches[s_error] = p_error
    return matches

def run_and_check_test_data(students_filename: str, projects_filename: str, match_errors: dict = {}) -> (bool, str):
    ''' "Test engine" that BOTH runs and checks algorithm given input files.
        Parameters:
            students_filename (str): filename for students' project preference list
            projects_filename (str): filename for projects' student preference list
        Optional parameters:
            match_errors (dict): inject errors into matches to test failing modes
        Returns:
            Tuple:
                bool: True or False result of a valid stable match, for unit test assert statement
                str: Informative message about result
    '''

    # Input files processing [app.py]
    students_filename = TEST_DATA_DIR + students_filename
    projects_filename = TEST_DATA_DIR + projects_filename

    # `with` for context management (opened file closes at end of statement)
    with open(students_filename, 'rb') as students_file, open(projects_filename, 'rb') as projects_file:
        # Create FileStorage objects (to match with Flask app code)
        students = FileStorage(students_file)
        projects = FileStorage(projects_file)
        # Convert to Pandas DataFrame (from app.py)
        students_df = parse_df_upload(students)
        projects_df = parse_df_upload(projects)

    # Prepare and validate inputs
    students_df, projects_df = validate_inputs(students_df, projects_df)

    # Run algorithm
    matches = matching_algorithm(students_df, projects_df)

    # Inject errors to test failing modes (none by default)
    matches = inject_errors(matches, match_errors)

    # Check algorithm (returns bool, string)
    return stable_match_checker(students_df, projects_df, matches)

##############
# Unit Tests #
##############

def test_td_1(students_filename = 'td_1_students.xlsx', projects_filename = 'td_1_projects.xlsx'):
    ''' Run and check test case: test data set 1'''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed

def test_td_2(students_filename = 'td_2_students.xlsx', projects_filename = 'td_2_projects.xlsx'):
    ''' Run and check test case: test data set 2'''
    result, message = run_and_check_test_data(students_filename, projects_filename)
    assert result, message
    print(message)  # otherwise, "PASS" message doesn't get printed

####################
# Validate Checker #
####################

@pytest.mark.skip()
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
