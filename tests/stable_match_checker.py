# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# stable_match_checker.py

import pandas as pd
from collections import defaultdict

def stable_match_checker(students_df, projects_df, matches) -> (bool, str):
    '''
        Checks for stable match according to Gaye-Shapley requirements
        Parameters:
            students_df (DataFrame): students' project preference list
            projects_df (DataFrame): projects' student preference list
            matches (dict): output from matching_algorithm to check for stable match
        Returns:
            bool: The result of the check. True = stable match. False = unstable or invalid
            string: Result details
    '''

    ##################################################
    # Set up data structures [matching_algorithm.py] #
    ##################################################
    # Initialize dictionaries for student and project preferences
    student_prefs = {}
    project_prefs = {}
    # Extract student preferences
    for _, row in students_df.iterrows():
        student_prefs[row['student_names']] = row[1:].dropna().tolist()
    # Extract project preferences
    for _, row in projects_df.iterrows():
        # Assuming the first two columns are 'project_name' and 'max_students'
        project_prefs[row['project_name']] = row[2:].dropna().tolist()
    # Map each project to its capacity
    project_capacity = projects_df.set_index('project_name')['max_students'].to_dict()

    ###################
    # Stable Matching #
    ###################
    # Definition: No unstable pairs defined as [lecture-5-algorithm-analysis, slide 5]:
    # "Applicant prefers hospital to the hospital it was assigned ...
    # ... That hospital prefers the applicant over one of its current students"
    # Extension: Multiple applicants (n) can be assigned per hospital/project (1)
    # Comment conventions: S - student, P - project, p - preferences list, m - match / matches list
    # TO-DO: control debug logging

    # Per S-P match loop
    print('\n')
    for s_matched, p_matched in matches.items():
        print(f'Checking for stable match: {s_matched} and {p_matched}')
        s_prefs = student_prefs[s_matched] # projects in order of student's preferences
        p_prefs = project_prefs[p_matched] # students in order of project's preferences

        # INVALID checks
        # TODO break into a function so that we can access from the Flask app
        if p_matched not in s_prefs:
            error_msg = f'INVALID: {p_matched} is not in {s_matched} preference list!'
            print(f'\t-> {error_msg}')
            return False, error_msg
        if s_matched not in p_prefs:
            error_msg = f'INVALID: {s_matched} is not in {p_matched} preference list!'
            print(f'\t-> {error_msg}')
            return False, error_msg

        # Per P in Sp list loop (until Pm)
        print(f'\t{s_matched} preference list: {s_prefs}')
        for p_check in s_prefs: # projects in order of student's preferences
            p_prefs = project_prefs[p_check] # students in order of project's preferences
            print(f'\t\tChecking {p_check} with preferences: {p_prefs}')

            # Break out of loop here: no need to check less preferred projects
            if p_check == p_matched:
                print(f'\t\t\t{s_matched} is in {p_check} preference list -> STABLE PAIR')
                break

            # Skip here if student is not on project's preference list at all
            if s_matched not in p_prefs:
                print(f'\t\t\t{s_matched} is not in {p_check} preference list, skip to next project in order')
                continue

            # Per Pp: check for S not more preferred than Pm
            check_if_matched = False
            for s_check in p_prefs: # students in order of project's preferences!
                if s_check == s_matched:
                    check_if_matched = True # start checking at next iteration
                    continue

                if check_if_matched: # checking less preferred students now
                    print(f'\t\t\t{s_check} is preferred less than {s_matched}')
                    if s_check in matches:
                        if matches[s_check] == p_check:
                            print(f'\t\t\t\t-> But {s_check} matched with {p_check}')
                            error_msg = f'UNSTABLE PAIR found: {s_matched} and {p_matched}'
                            print(f'\t\t\t\t-> {error_msg}')
                            return False, error_msg
                        else:
                            print(f'\t\t\t\tOKAY: {s_check} is matched with {matches[s_check]}')
                    else:
                        print(f'\t\t\t\tOKAY: {s_check} is unmatched')
                else:
                    print(f'\t\t\t{s_check} is preferred more than {s_matched}')

    ####################
    # Project Capacity #
    ####################
    # Check that Pm size <= Pmax

    # Re-build "project_assignments"
    project_assignments = defaultdict(list)
    for s_matched, p_matched in matches.items():
        project_assignments[p_matched].append(s_matched)

    # Check assignments vs. capacities
    for p in project_assignments:
        p_matches = project_assignments[p]
        p_max = project_capacity[p]
        print(f'Checking project capacity for {p} with {p_matches} vs. max {p_max} ...')
        if len(p_matches) > p_max:
            error_msg = f'INVALID: {p} has more students than capacity of {p_max}'
            print(f'\t-> {error_msg}')
            return False, error_msg

    # IF code reached here, there are no unstable nor invalid pairs!
    return True, 'STABLE: no unstable pairs found'
