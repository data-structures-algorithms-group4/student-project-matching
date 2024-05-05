# Student-Project Matching

## Overview

This project helps students find suitable matches with their preferred projects based on their preferences and the project requirements.

Abraham, David J., Robert W. Irving, and David F. Manlove. “Two Algorithms for the Student-Project Allocation Problem.” Journal of Discrete Algorithms 5, no. 1 (March 1, 2007): 73–90. https://doi.org/10.1016/j.jda.2006.03.006.

## Matching Algorithm Pseudocode

### Initialization
1. **Load Data:**
   - Extract student and project information.
   - Initialize dictionaries for student preferences (`student_prefs`), project preferences (`project_prefs`), project capacities (`project_capacity`), and project availability (`project_availability`).

2. **Setup Structures:**
   - Prepare `matches` dictionary to track which student is assigned to which project.
   - Initialize `project_assignments` to manage lists of students assigned to each project.

3. **Prepare Student Queue:**
   - Enqueue all students into `unassigned_students` for processing.

### Algorithm Execution
1. **Process Unassigned Students:**
   - While there are students in `unassigned_students`:
     - Dequeue a student and attempt to assign them to a project based on their preferences.

2. **Assignment Attempt:**
   - For each preferred project of the current student:
     - If the project has available capacity and the student fits the project’s preference criteria:
       - **Assign** the student to the project.
       - Update `matches` and `project_assignments`.
       - Reduce availability by 1 in `project_availability`.
     - If no direct assignment is possible:
       - **Reevaluate Project Assignments:**
         - Consider potential new assignments including the current student.
         - Sort all current and new assignees by preference.
         - Retain assignees within project capacity and displace the rest.
         - Update `matches` and `project_assignments` accordingly.

3. **Handle Reassignments and Requeued Students:**
   - Requeue displaced students not matched and not already requeued to ensure all students are considered for any new available spots as projects reevaluate assignments.

### Finalization
- Return the `matches` dictionary showing the assignment of students to projects after all possible assignments and reevaluations are complete.

See Abraham, David J., Robert W. Irving, and David F. Manlove. “Two Algorithms for the Student-Project Allocation Problem.” Journal of Discrete Algorithms 5, no. 1 (March 1, 2007): 73–90. https://doi.org/10.1016/j.jda.2006.03.006.


## Stable Matching

Given a set of n proposers (students) and recipients (projects), each with their own preferences, our goal following the Gale-Shapley algorithm was to to find an assignment such that: Each student ends up with exactly one project. In this case a project may allocate more than one student, but not vice versa. This is known as a stable matching. Its applications range from economics and networks to medical school assignments. The Gale-Shapley Algorithm proposes a greedy solution to this. We process students arbitrarily and go down each proposer's list of preferences for recipients. In each round, if a recipient is free, this (proposer, recipient) pair becomes temporarily "engaged". If the recipient is already engaged, it will leave (and thus free) its current partner only if it prefers this proposer more. This process continues until all n proposers and recipients are engaged with one other person. It is proven to produce a unique and optimal solution. It runs in quadratic time. For more information visit gale-shapley.com.

