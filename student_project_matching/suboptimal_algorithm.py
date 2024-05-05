import pandas as pd
from collections import defaultdict
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def preprocess_preferences(students_df, projects_df):
    students = students_df["student_names"].tolist()
    projects = projects_df["project_names"].tolist()
    project_capacity = projects_df.set_index("project_names")["max_students"].to_dict()
    project_availability = project_capacity.copy()

    student_prefs = {}
    for _, row in students_df.iterrows():
        student = row["student_names"]
        student_prefs[student] = [(proj, rank) for rank, proj in enumerate(row[1:].dropna().tolist(), start=1)]

    project_prefs = {}
    for _, row in projects_df.iterrows():
        project = row["project_names"]
        project_prefs[project] = [(stud, rank) for rank, stud in enumerate(row[2:].dropna().tolist(), start=1)]

    return students, projects, student_prefs, project_prefs, project_capacity, project_availability


def assign_student_to_project(student, project, matches, project_assignments, project_availability):
    logging.info(f'Assigning {student} to {project}.')
    matches[student] = project
    project_assignments[project].append(student)
    project_availability[project] -= 1
    logging.info(f'Updated availability for {project}: {project_availability[project]}.')


def reevaluate_assignments(project, project_prefs, project_assignments, project_availability, matches):
    logging.info(f'Reevaluating {project}')
    current_assignees = project_assignments[project]
    sorted_assignees = sorted(current_assignees,
                              key=lambda s: next((rank for stud, rank in project_prefs[project] if stud == s),
                                                 float('inf')))

    to_keep = project_availability[project]
    project_assignments[project] = sorted_assignees[:to_keep]
    displaced_students = sorted_assignees[to_keep:]

    for student in displaced_students:
        logging.info(f'Displacing {student} from {project}')
        matches.pop(student, None)
        if student in project_assignments[project]:
            project_assignments[project].remove(student)

    logging.info(f'Updated project assignments for {project}: {project_assignments[project]}')
    return displaced_students


def suboptimal_algorithm(students_df, projects_df):
    students, projects, student_prefs, project_prefs, project_capacity, project_availability = preprocess_preferences(
        students_df, projects_df)

    matches = {}
    project_assignments = defaultdict(list)
    unassigned_students = students[:]

    while unassigned_students:
        next_round_students = []
        for student in unassigned_students:
            assigned = False
            if student not in matches:
                for project, _ in student_prefs[student]:
                    logging.info(
                        f'Checking project {project} for student {student} with availability {project_availability[project]}')

                    if project in project_prefs and any(stud == student for stud, _ in project_prefs[project]):
                        if project_availability[project] > 0:
                            assign_student_to_project(student, project, matches, project_assignments,
                                                      project_availability)
                            assigned = True
                            break
                        else:
                            displaced = reevaluate_assignments(project, project_prefs, project_assignments,
                                                               project_availability, matches)
                            next_round_students.extend(displaced)
                            if student not in matches:
                                next_round_students.append(student)
                            assigned = True
                            break

            if not assigned:
                next_round_students.append(student)
        unassigned_students = list(set(next_round_students))

        logging.info(f'Updated unassigned students: {unassigned_students}')

    return matches
