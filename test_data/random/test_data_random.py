# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# test_data_random.py

import random
import csv

def generate_random_students_projects(num_students=201, num_projects=201, num_choices=3, max_students_range=5, write_csv=True):
    '''Generate random students, projects, and preference lists based on size inputs.
       Original code: test_data_random.ipynb'''

    # Define project names and capacities
    project_names = ['p{}'.format(i) for i in range(1, num_projects + 1)]
    max_students = [random.randint(1, max_students_range) for _ in range(num_projects)]
    students = ['s{}'.format(i) for i in range(1, num_students + 1)]

    # Generate student preference data
    student_preferences = {student: random.sample(project_names, num_choices) for student in students}

    # Define the project data with initial capacities and empty slots for student assignments
    project_data = {project: {'max_students': cap, 'assigned_students': []} for project, cap in zip(project_names, max_students)}

    # Create a shuffled list of all student preferences
    all_preferences = []
    for student, preferences in student_preferences.items():
        for preference in preferences:
            all_preferences.append((student, preference))
    random.shuffle(all_preferences)  # Shuffle to ensure fair assignment chances

    # Function to assign students to their preferred projects without duplications within the same project
    def initial_assignment():
        assigned_students = set()  # Keep track of which students have been assigned
        for student, preference in all_preferences:
            if len(project_data[preference]['assigned_students']) < project_data[preference]['max_students'] and student not in assigned_students:
                project_data[preference]['assigned_students'].append(student)
                assigned_students.add(student)

    # Function to fill under-capacity projects with any available students
    def fill_under_capacity_projects():
        for project, details in project_data.items():
            while len(details['assigned_students']) < details['max_students']:
                possible_students = set(students) - set(details['assigned_students'])
                if not possible_students:
                    break
                student = random.choice(list(possible_students))
                details['assigned_students'].append(student)

    # Assign students to projects
    initial_assignment()
    fill_under_capacity_projects()

    # Save student preferences to CSV
    if write_csv:
        with open('student_preferences.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write column names for preferences
            pref_columns = ['{}st_choice'.format(i+1) for i in range(num_choices)]
            writer.writerow(['student_names'] + pref_columns)
            # Write student preferences
            for student, prefs in student_preferences.items():
                row = [student] + prefs
                writer.writerow(row)

    # Save project assignments to CSV
    if write_csv:
        with open('project_assignments.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['project_names', 'max_students'] + ['{}st_choice'.format(i+1) for i in range(max_students_range)])
            for project, details in project_data.items():
                # Separate assigned students into multiple columns for each choice
                assigned_students = details['assigned_students']
                row = [project, details['max_students']]
                for i in range(num_choices):
                    if i < len(assigned_students):
                        row.append(assigned_students[i])
                    else:
                        row.append("")  # Fill empty if no more assigned students
                writer.writerow(row)

    # Read CSV and extract column names
    #with open('student_preferences.csv', newline='') as csvfile:
    #    reader = csv.reader(csvfile)
    #    student_names = next(reader)

    # Extract column names
    student_columns = ['student_names'] + ['{}st_choice'.format(i + 1) for i in range(num_choices)]
    project_columns = ['project_names', 'max_students'] + ['{}st_choice'.format(i + 1) for i in range(max_students_range)]

    # Return the generated data and extracted column names
    return student_preferences, project_data, student_columns, project_columns
