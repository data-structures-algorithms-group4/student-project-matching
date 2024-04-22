import pandas as pd
from collections import defaultdict, deque

def preprocess_preferences(students_df, projects_df):
    students = students_df["student_names"].tolist()
    projects = projects_df["project_names"].tolist()

    # Project capacity
    project_capacity = projects_df.set_index("project_names")["max_students"].to_dict()

    # Preprocess student preferences into numerical ranks
    student_prefs = {row["student_names"]: deque(sorted(((proj, rank) for rank, proj in enumerate(row[1:].dropna().tolist(), start=1)), key=lambda x: x[1]))
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
    # Get all current assignees and add the currently considered student
    current_assignees = project_assignments[project]
    preferred_assignees = sorted(current_assignees, key=lambda s: project_prefs[project].get(s, float('inf')))

    # Enforce project capacity by retaining only the top-preferred students within capacity limits
    if len(preferred_assignees) > project_availability[project]:
        # Students who cannot be accommodated due to capacity are removed from the project
        for student in preferred_assignees[project_availability[project]:]:
            del matches[student]  # Remove these students from matches
            project_assignments[project].remove(student)  # Remove from project assignments

        preferred_assignees = preferred_assignees[:project_availability[project]]

    project_assignments[project] = preferred_assignees

def matching_algorithm(students_df, projects_df):
    students, projects, student_prefs, project_prefs, project_capacity, project_availability = preprocess_preferences(students_df, projects_df)

    matches = {}
    project_assignments = defaultdict(list)
    unassigned_students = deque(students)

    while unassigned_students:
        student = unassigned_students.popleft()
        while student_prefs[student]:
            project, _ = student_prefs[student].popleft()  # Unpack the project and rank from the deque
            if student in project_prefs[project] and project_availability[project] > 0:
                assign_student_to_project(student, project, matches, project_assignments, project_availability)
                break
            elif student in project_prefs[project]:
                # Reevaluate assignments if the project is at full capacity
                displaced = reevaluate_assignments(project, project_prefs, project_assignments, project_availability, matches)
                if student not in matches:  # If student is not matched
                    unassigned_students.append(student)
                if displaced:  # Requeue displaced students
                    for d_student in displaced:
                        unassigned_students.append(d_student)
                break

    return matches

