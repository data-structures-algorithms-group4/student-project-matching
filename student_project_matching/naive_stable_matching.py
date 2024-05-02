import random
from collections import defaultdict, deque
import logging
from tests.stable_match_checker import stable_match_checker
def naive_stable_matching(students_df, projects_df):
    """
    Attempts to randomly match students to projects, checking for stability,
    and repeats this until a stable match is found or a certain number of attempts is reached.

    Parameters:
        students_df (DataFrame): DataFrame containing student names and their preferences.
        projects_df (DataFrame): DataFrame containing project names, capacities, and their preferences.

    Returns:
        dict: A dictionary mapping students to projects in a stable configuration if found.
    """
    students = students_df['student_names'].tolist()
    projects = projects_df['project_names'].tolist()
    project_capacity = projects_df.set_index('project_names')['max_students'].to_dict()

    # Function to generate a random match considering project capacities
    def generate_random_match():
        matches = {}
        project_assignments = defaultdict(list)
        all_students = deque(students)
        random.shuffle(all_students)  # Shuffle to ensure randomness

        while all_students:
            student = all_students.popleft()
            possible_projects = [p for p in projects if len(project_assignments[p]) < project_capacity[p]]
            if possible_projects:
                chosen_project = random.choice(possible_projects)
                matches[student] = chosen_project
                project_assignments[chosen_project].append(student)

        return matches

    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Check for stability and repeat if not stable
    stable = False
    matches = {}
    attempts = 0
    while not stable and attempts < 1000000:  # Limit attempts to prevent infinite loops
        matches = generate_random_match()
        stable, message = stable_match_checker(students_df, projects_df, matches)
        attempts += 1
        logging.info(f'Attempt {attempts}: {message}')
    
    if not stable:
        logging.warning("Failed to find a stable match within 1000000 attempts.")
    else:
        logging.info("Stable match found.")
    
    return matches
