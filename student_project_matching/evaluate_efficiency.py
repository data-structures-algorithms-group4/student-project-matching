# Data Structures & Algorithms Spring 2024
# Group 4: Student-Project Matching
# evaluate_efficiency.py

# Libraries
import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Custom project functions
from test_data.random.test_data_random import generate_random_students_projects
from tests.testing_environment import validate_inputs, config_logging
from student_project_matching import matching_algorithm, suboptimal_algorithm
from tests.stable_match_checker import stable_match_checker

################################################
# Evaluate time complexity as input size grows #
################################################

def compare_algorithm_times(input_size_n, algorithms):
    '''Takes input size "n" and a list of different algorithms (as functions) for comparing run times
       on the SAME randomly generated dataset of students and projects.
       Returns a list of algorithm run times, one per-algorithm.'''

    # Currently same "n" for all input parameters but can adjust!
    student_preferences, project_data, student_columns, project_columns = generate_random_students_projects(
        num_students=input_size_n,
        num_projects=input_size_n,
        num_choices=input_size_n,
        max_students_range=input_size_n,
        write_csv=False)

    # Construct students Dataframe
    students_df = pd.DataFrame(student_preferences).T.reset_index()
    students_df.columns = student_columns

    # Construct projects DataFrame
    projects_df_initial = pd.DataFrame(project_data).T.reset_index()
    projects_df_s_list = pd.DataFrame(projects_df_initial['assigned_students'].tolist())
    projects_df = pd.concat([projects_df_initial.iloc[:, 0:2], projects_df_s_list], axis=1)
    projects_df.columns = project_columns[0:2 + projects_df_s_list.shape[1]]

    # Input validation
    result, message = validate_inputs(students_df, projects_df)
    assert result, message  # Failed validation

    # Loop through algorithms
    algo_times = list()
    for algorithm in algorithms:

        # Run algorithm and check run-time
        #config_logging('evaluate_efficiency.log', 'DEBUG') # DO NOT RUN FOR TIMES!
        algo_t0 = time.time()
        matches = algorithm(students_df, projects_df) # RUN THIS ALGORITHM!!
        algo_t1 = time.time()
        algo_times.append(algo_t1 - algo_t0)

        # Check algorithm # DO NOT RUN FOR TIMES!
        #result, message = stable_match_checker(students_df, projects_df, matches)
        #assert result, message

    return algo_times

#################
# Main run code #
#################

# Loop setup values
input_sizes = np.logspace(0, 4, 25).astype(int)[0:21] #[1, ..., 10, ..., 100, ..., 1000, ..., 10000]
algorithm_list = [matching_algorithm.matching_algorithm]
#algorithm_list = [matching_algorithm.matching_algorithm, suboptimal_algorithm.matching_algorithm]

# Data structure to save times
algo_times_dict = dict()

for input_size_n in input_sizes:
    algo_times = compare_algorithm_times(input_size_n, algorithm_list)
    algo_times_dict[input_size_n] = algo_times
    print(f'Input {input_size_n}, times {algo_times}')

#TO-DO: handle for list of 2+ algorithm times
algo_times_df = pd.DataFrame(algo_times_dict).T.reset_index()
algo_times_df.columns = ['Input size n', 'Run-time (seconds)']

# Visualize n vs. t
sns.lineplot(data=algo_times_df, x='Input size n', y='Run-time (seconds)', marker='o')
plt.title('Time efficiency of student-project matching algorithms')
#plt.show()
plt.savefig('evaluate_efficiency.png')