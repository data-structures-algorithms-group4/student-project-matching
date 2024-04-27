import pandas as pd


# We do not want error messages for empty cells in the spreadsheet people upload
# Pandas converts empty cells ("") to nan
def ignore_missings(row):
    return [col for col in row if not pd.isna(col)]


def check_duplicates(row):
    row = ignore_missings(row)
    return len(row) == len(set(row))
    

def validate_students_df(df):
    """
    1st column is students and must be unique
    Every column after that is preferences and cannot be repeated
    """
    # check that students are unique
    if not df["student_names"].is_unique:
        return False, "Not all students are unique"
    # check that preferences are unique
    # set() reduces to unique elements
    # assumes that project names != student names
    if not df.apply(check_duplicates, axis=1).all():
        return False, "Not all preferences within student are unique"
    return True, ""


def validate_projects_df(df):
    """
    1st column is projects and must be unique
    2nd column is max capacity and must be numeric and greater than zero
    Every column after that is preferences and cannot be repeated
    """
    if not df["project_names"].is_unique:
        return False, "Not all projects are unique"
    if not df["max_students"].apply(lambda x: isinstance(x, int) and x > 0).all():
        return False, "max_students is not always an integer greater than zero"
    # check that preferences are unique
    # set() reduces to unique elements
    # assumes that student names != project names or max_capacity
    if not df.apply(check_duplicates, axis=1).all():
        return False, "Not all preferences within project are unique"
    return True, ""


def validate_students_projects(students_df, projects_df):
    """
    Confirms that:
    All projects in students_df appear in projects_df
    All students in projects_df appear in students_df
    """
    students_from_students_df = set(ignore_missings(students_df["student_names"].values))
    projects_from_students_df = set(ignore_missings(students_df.iloc[:, 1:].values.ravel()))
    projects_from_project_df = set(ignore_missings(projects_df["project_names"].values))
    students_from_project_df = set(ignore_missings(projects_df.iloc[:, 2:].values.ravel()))
    if not projects_from_students_df.issubset(projects_from_project_df):
        return False, "Some projects in the student file are not in the projects file"
    if not students_from_project_df.issubset(students_from_students_df):
        return False, "Some students in the project file are not in the students file"
    return True, ""