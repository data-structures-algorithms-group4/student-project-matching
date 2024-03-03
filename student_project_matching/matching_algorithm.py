import pandas as pd
from collections import defaultdict

def matching_algorithm(students_df, projects_df):
    students = students_df['student_names'].tolist()
    projects = projects_df['project_name'].tolist()
    # Map each project to its capacity
    project_capacity = projects_df.set_index('project_name')['max_students'].to_dict()
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
    ### Matching algorithm
    # Initialize matching and availability:
    matches = {} # maps each student to their assigned project
    project_assignments = defaultdict(list) # keys are project names and values are lists of students assigned to each project: dynamically updated
    # Iteratively assign students to projects based on preferences and capacity
    while len(matches) < len(students):
        for student in students: # loop continues until all students have been assigned to a project
            if student not in matches: # iterates over each student who hasn't been matched yet
                for project in student_prefs[student]: # goes through each student's project preferences in order from most preferred to least preferred
                    if len(project_assignments[project]) < project_capacity[project] and student in project_prefs[project]: # check capacities and preferences
                        matches[student] = project
                        project_assignments[project].append(student)
                        break
                    else:
                        # Handling over-subscription with bidirectional preference consideration
                        # At capacity: evaluates if the new student could be more preferred compared to current assignees
                        if student in project_prefs[project]:
                            current_assignees = project_assignments[project]
                            # Include the new student for comparison while respecting project preferences
                            all_prefs = [s for s in project_prefs[project] if s in current_assignees + [student]]
                            preferred_assignees = sorted(current_assignees + [student], key=lambda x: all_prefs.index(x))[:project_capacity[project]] # ChatGPT suggestion
                            
                            if student in preferred_assignees: # if the new student is more preferred than the current assignees, adjust
                                new_assignees = preferred_assignees
                                for s in current_assignees:
                                    if s not in new_assignees:
                                        project_assignments[project].remove(s)
                                        del matches[s]
                                if student not in project_assignments[project]:
                                    project_assignments[project].append(student) # update assignments
                                    matches[student] = project
                                break
    return matches