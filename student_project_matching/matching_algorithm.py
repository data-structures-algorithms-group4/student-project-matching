import pandas as pd
from collections import defaultdict, deque

def preprocess_preferences(students_df, projects_df):
    students = students_df["student_names"].tolist()
    projects = projects_df["project_names"].tolist()

    # Project capacity
    project_capacity = projects_df.set_index("project_names")["max_students"].to_dict()

    # Preprocess student preferences into numerical ranks
    student_prefs = {
        row["student_names"]: deque(sorted(
            ((proj, rank) for rank, proj in enumerate(row[1:].dropna().tolist(), start=1)),
            key=lambda x: x[1]
        )) for _, row in students_df.iterrows()
    }

    # Preprocess project preferences similarly
    project_prefs = {
        row["project_names"]: {
            stud: rank for rank, stud in enumerate(row[2:].dropna().tolist(), start=1)
        } for _, row in projects_df.iterrows()
    }

    # Track project availability
    project_availability = {project: capacity for project, capacity in project_capacity.items()}

    return students, projects, student_prefs, project_prefs, project_capacity, project_availability

def assign_student_to_project(student, project, matches, project_assignments, project_availability):
    print(f"Assigning {student} to {project}.")
    matches[student] = project
    project_assignments[project].append(student)
    project_availability[project] -= 1
    print(f"Updated availability for {project}: {project_availability[project]}.")

def reevaluate_assignments(project, project_prefs, project_assignments, project_availability, matches, project_capacity, new_student=None):
    print(f"Reevaluating {project} with potential addition of {new_student}")
    current_assignees = list(project_assignments[project])
    if new_student:
        current_assignees.append(new_student)

    # Sort by preference and only displace the necessary number of students
    sorted_assignees = sorted(current_assignees, key=lambda s: project_prefs[project].get(s, float('inf')))
    kept_assignees = sorted_assignees[:project_capacity[project]]
    displaced_students = sorted_assignees[project_capacity[project]:]

    # Update the project assignments
    project_assignments[project] = kept_assignees
    for student in displaced_students:
        if student in matches:
            print(f"Displacing {student} from {project}")
            matches.pop(student)

    # Re-add only those who are kept
    for student in kept_assignees:
        matches[student] = project

    project_availability[project] = project_capacity[project] - len(kept_assignees)
    print(f"Updated project assignments for {project}: {project_assignments[project]}")
    return displaced_students

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
                displaced = reevaluate_assignments(project, project_prefs, project_assignments, project_availability, matches, project_capacity, student)
                if student not in matches:  # If student is not matched
                    unassigned_students.append(student)
                if displaced:  # Requeue displaced students
                    for d_student in displaced:
                        unassigned_students.append(d_student)
                break

    return matches