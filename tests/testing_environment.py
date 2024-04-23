# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# testing_environment.py

import pandas as pd
from student_project_matching.matching_algorithm import matching_algorithm
from tests.stable_match_checker import stable_match_checker
from student_project_matching.app import parse_df_upload
from student_project_matching.app import validate_students_df, validate_projects_df, validate_students_projects
from werkzeug.datastructures import FileStorage

# Constant for now
# TO-DO: change if we need to break up test data between algorithm and input validation
TEST_DATA_DIR = '../test_data/'

##########################
# Test Environment Setup #
##########################

def preprocess_inputs(students_df, projects_df):
    ''' Pre-process inputs before inputting them to algorithm (from app.py)'''
    # 1. Force column names to agree with algorithm expectations
    students_df = students_df.rename(
        columns={students_df.columns[0]: "student_names"}
    )
    projects_df = projects_df.rename(
        columns={
            projects_df.columns[0]: "project_names",
            projects_df.columns[1]: "max_students",
        }
    )
    # 2. Numericalize project max capacity
    projects_df["max_students"] = pd.to_numeric(projects_df["max_students"])
    return students_df, projects_df

def validate_inputs(students_df, projects_df) -> (bool, str):
    ''' Validate inputs before inputting them to algorithm (from app.py)'''

    # Student-project lists
    result, message = validate_students_df(students_df)
    if not result: return result, message #Failed validation

    # Project-student lists
    result, message = validate_projects_df(projects_df)
    if not result: return result, message  # Failed validation

    # Students<->Projects coherency
    result, message = validate_students_projects(students_df, projects_df)
    if not result: return result, message  # Failed validation

    return True, ""

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

    # Pre-process inputs
    students_df, projects_df = preprocess_inputs(students_df, projects_df)

    # Validate inputs
    result, message = validate_inputs(students_df, projects_df)
    if not result: return result, message  # Failed validation

    # Run algorithm
    matches = matching_algorithm(students_df, projects_df)

    print("Matching Results:")
    for student, project in matches.items():
        print(f"{student} is assigned to {project}")

    # Inject errors to test failing modes (none by default)
    matches = inject_errors(matches, match_errors)

    # Check algorithm (returns bool, string)
    return stable_match_checker(students_df, projects_df, matches)