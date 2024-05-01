import time

# Assume original_matching_algorithm and optimized_matching_algorithm are defined
# Assume students_df and projects_df are your DataFrames

start_time_original = time.time()
original_matches = matching_algorithm(students_df, projects_df)
end_time_original = time.time()

start_time_optimized = time.time()
optimized_matches = matching_algorithm_opt(students_df, projects_df)
end_time_optimized = time.time()

print(f"Original algorithm time: {end_time_original - start_time_original} seconds")
print(f"Optimized algorithm time: {end_time_optimized - start_time_optimized} seconds")