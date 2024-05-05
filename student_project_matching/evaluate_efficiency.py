# Libraries
import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Custom project functions
from test_data.random.test_data_random import generate_random_students_projects
from tests.testing_environment import validate_inputs, config_logging
from student_project_matching.matching_algorithm import matching_algorithm
from student_project_matching.suboptimal_algorithm import suboptimal_algorithm
from student_project_matching.naive_stable_matching import naive_stable_matching
from tests.stable_match_checker import stable_match_checker

def compare_algorithm_times(input_size_n, algorithms):
    '''Takes input size "n" and a list of different algorithms (as functions) for comparing run times
       on the SAME randomly generated dataset of students and projects.
       Returns a list of algorithm run times, one per-algorithm.'''

    student_preferences, project_data, student_columns, project_columns = generate_random_students_projects(
        num_students=input_size_n,
        num_projects=input_size_n,
        num_choices=input_size_n,
        max_students_range=input_size_n,
        write_csv=False)

    students_df = pd.DataFrame(student_preferences).T.reset_index()
    students_df.columns = student_columns

    projects_df_initial = pd.DataFrame(project_data).T.reset_index()
    projects_df_s_list = pd.DataFrame(projects_df_initial['assigned_students'].tolist())
    projects_df = pd.concat([projects_df_initial.iloc[:, 0:2], projects_df_s_list], axis=1)
    projects_df.columns = project_columns[0:2 + projects_df_s_list.shape[1]]

    result, message = validate_inputs(students_df, projects_df)
    assert result, message  # Failed validation

    algo_times = list()
    for algorithm in algorithms:
        algo_t0 = time.time()
        matches = algorithm(students_df, projects_df) # RUN THIS ALGORITHM!!
        algo_t1 = time.time()
        algo_times.append(algo_t1 - algo_t0)

    return algo_times

# Logging config
log_level = 'CRITICAL'
config_logging('evaluate_efficiency.log', log_level)

# Graph 1: Suboptimal vs. Matching Algorithm
input_sizes = np.logspace(0, 4, 25).astype(int)
input_sizes_1 = input_sizes[0:21]
algorithm_list_1 = [matching_algorithm, suboptimal_algorithm]

algo_times_dict_1 = {}
for input_size_n in input_sizes_1:
    algo_times = compare_algorithm_times(input_size_n, algorithm_list_1)
    algo_times_dict_1[input_size_n] = algo_times
    print(f'Graph 1 - Input size {input_size_n}, algorithm times {algo_times}')

algo_times_df_1 = pd.DataFrame(algo_times_dict_1).T.reset_index()
algo_times_df_1.columns = ['input_size_n', 'suboptimal', 'matching']

sns.lineplot(data=algo_times_df_1, x='input_size_n', y='suboptimal', marker='o', label='Matching Algorithm')
sns.lineplot(data=algo_times_df_1, x='input_size_n', y='matching', marker='o', label='Suboptimal Algorithm')
plt.yscale('log')
plt.title('Comparison of Matching Algorithm vs. Suboptimal Algorithm (Log scale)')
plt.xlabel('Input size (number of students/projects)')
plt.ylabel('Run time (seconds, log scale)')
plt.savefig('matching_vs_suboptimal.png')
plt.clf()

# Graph 2: Matching vs. Naive Stable Algorithm
input_sizes_2 = input_sizes[0:6]
algorithm_list_2 = [matching_algorithm, naive_stable_matching]

algo_times_dict_2 = {}
for input_size_n in input_sizes_2:
    algo_times = compare_algorithm_times(input_size_n, algorithm_list_2)
    algo_times_dict_2[input_size_n] = algo_times
    print(f'Graph 2 - Input size {input_size_n}, algorithm times {algo_times}')

algo_times_df_2 = pd.DataFrame(algo_times_dict_2).T.reset_index()
algo_times_df_2.columns = ['input_size_n', 'matching', 'naive']

sns.lineplot(data=algo_times_df_2, x='input_size_n', y='matching', marker='o', label='Efficient Algorithm')
sns.lineplot(data=algo_times_df_2, x='input_size_n', y='naive', marker='o', label='Naive Algorithm')
plt.yscale('log')
plt.title('Comparison of Matching vs. Naive Algorithm (Log scale)')
plt.xlabel('Input size (number of students/projects)')
plt.ylabel('Run time (seconds, log scale)')
plt.savefig('matching_vs_naive.png')
