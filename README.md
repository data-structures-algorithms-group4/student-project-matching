# Student-Project Matching

## Overview

This project helps students find suitable matches with their preferred projects based on their preferences and the project requirements.

### Algorithm in Pseudocode

Abraham, David J., Robert W. Irving, and David F. Manlove. “Two Algorithms for the Student-Project Allocation Problem.” Journal of Discrete Algorithms 5, no. 1 (March 1, 2007): 73–90. https://doi.org/10.1016/j.jda.2006.03.006.

Initialize structures from data:
    students, projects, student_prefs, project_prefs, project_capacity, project_availability

Create empty structures for tracking:
    matches, project_assignments

Queue all students for processing:
    unassigned_students

While there are unassigned students:
    Process each student from the queue:
        While student has unpreferred projects and is not processed:
            Attempt to assign student to their next preferred project:
                If project has available capacity:
                    Assign student
                    Mark student as processed
                Else:
                    Reevaluate project assignments:
                        Consider all current and potentially new assignees
                        Sort by preference
                        Displace students exceeding capacity
                        Update assignments and availability
                        Handle requeued and displaced students
Return final matches



## Stable Matching

Given a set of n proposers (students) and recipients (projects), each with their own preferences, our goal following the Gale-Shapley algorithm was to to find an assignment such that: Each student ends up with exactly one project. In this case a project may allocate more than one student, but not vice versa. This is known as a stable matching. Its applications range from economics and networks to medical school assignments. The Gale-Shapley Algorithm proposes a greedy solution to this. We process students arbitrarily and go down each proposer's list of preferences for recipients. In each round, if a recipient is free, this (proposer, recipient) pair becomes temporarily "engaged". If the recipient is already engaged, it will leave (and thus free) its current partner only if it prefers this proposer more. This process continues until all n proposers and recipients are engaged with one other person. It is proven to produce a unique and optimal solution. It runs in quadratic time. For more information visit gale-shapley.com.

