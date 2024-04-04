import pandas as pd
from collections import defaultdict, deque

def preprocess_preferences(students_df, projects_df):
    students = students_df["student_names"].tolist()
    projects = projects_df["project_names"].tolist()

    # Project capacity
    project_capacity = projects_df.set_index("project_names")["max_students"].to_dict()

    # Preprocess student preferences into numerical ranks
    student_prefs = {row["student_names"]: {proj: rank for rank, proj in enumerate(row[1:].dropna().tolist(), start=1)}
                     for _, row in students_df.iterrows()}

    # Preprocess project preferences similarly
    project_prefs = {row["project_names"]: {stud: rank for rank, stud in enumerate(row[2:].dropna().tolist(), start=1)}
                     for _, row in projects_df.iterrows()}

    # Track project availability
    project_availability = {project: capacity for project, capacity in project_capacity.items()}

    return students, projects, student_prefs, project_prefs, project_capacity, project_availability


def assign_student_to_project(student, project, matches, project_assignments, project_availability):
    matches[student] = project
    project_assignments[project].append(student)
    project_availability[project] -= 1


def reevaluate_assignments(project, project_prefs, project_assignments, project_availability, matches):
    # Sort current assignees by preference, then cut off to respect project capacity
    sorted_assignees = sorted(project_assignments[project], key=lambda s: project_prefs[project].get(s, float('inf')))
    project_assignments[project] = sorted_assignees[:project_availability[project]]

    # Update matches based on adjusted assignments
    for student in list(matches):
        if student not in project_assignments[project]:
            del matches[student]


def matching_algorithm(students_df, projects_df):
    students, projects, student_prefs, project_prefs, project_capacity, project_availability = preprocess_preferences(
        students_df, projects_df)

    matches = {}
    project_assignments = defaultdict(list)
    unassigned_students = deque(students)

    while unassigned_students:
        student = unassigned_students.popleft()
        for project, _ in sorted(student_prefs[student].items(), key=lambda item: item[1]):
            if project_availability[project] > 0:
                assign_student_to_project(student, project, matches, project_assignments, project_availability)
                break
            elif student in project_prefs[project]:
                # Reevaluate based on preferences if at capacity
                reevaluate_assignments(project, project_prefs, project_assignments, project_availability, matches)
                if student not in matches:
                    unassigned_students.append(student)  # Re-queue student for reassignment if they were displaced
                break

    return matches
