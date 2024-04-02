import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
    render_template,
)
from werkzeug.utils import secure_filename
import pandas as pd
from student_project_matching.matching_algorithm import matching_algorithm
from io import StringIO
from functools import wraps

# TODO find a better solution than manually going up one directory with "../"
UPLOAD_FOLDER = "../student_project_matching/uploads"
# TODO add support for CSV
ALLOWED_EXTENSIONS = {"txt", "xlsx", "csv"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "NOT-A-SECRET-ONLY-USE-FOR-LOCAL-TESTING"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def file_type(filename):
    return filename.rsplit(".", 1)[1].lower()


def allowed_file(filename):
    return file_type(filename) in ALLOWED_EXTENSIONS


def txt_to_df(txt_file):
    txt_file.seek(0)
    file_contents = txt_file.read().decode("utf-8")
    file_contents = file_contents.splitlines()
    file_contents = [line.split(" ") for line in file_contents]
    df = pd.DataFrame(file_contents)
    return df


class InputValidationError(Exception):
    pass


def validate_students_df(df):
    """
    1st column is students and must be unique
    Every column after that is preferences and cannot be repeated
    """
    # check that students are unique
    if not df["student_names"].is_unique:
        raise InputValidationError("Not all students are unique")
    # check that preferences are unique
    # set() reduces to unique elements
    # assumes that project names != student names
    if not df.apply(lambda row: len(row) == len(set(row)), axis=1).all():
        raise InputValidationError("Not all preferences within student are unique")


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
    if not df.apply(lambda row: len(row) == len(set(row)), axis=1).all():
        return False, "Not all preferences within project are unique"
    return True, ""


# TODO function that validates the combination of students and projects
def validate_students_projects(students_df, projects_df):
    """
    Confirms that:
    All projects in students_df appear in projects_df
    All students in projects_df appear in students_df
    """
    students_from_students_df = set(students_df["student_names"].values)
    projects_from_students_df = set(students_df.iloc[:, 1:].values.ravel())
    projects_from_project_df = set(projects_df["project_names"].values)
    students_from_project_df = set(projects_df.iloc[:, 2:].values.ravel())
    if not projects_from_students_df.issubset(projects_from_project_df):
        return False, "Some projects in the student file are not in the projects file"
    if not students_from_project_df.issubset(students_from_students_df):
        return False, "Some students in the project file are not in the students file"
    return True, ""


def parse_df_upload(file):
    if file_type(file.filename) == "txt":
        df = txt_to_df(file)
    if file_type(file.filename) == "xlsx":
        df = pd.read_excel(file)
    if file_type(file.filename) == "csv":
        file.seek(0)
        df = pd.read_csv(file, header=0)
    return df


def input_validation_decorator(*validators):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Only validate for POST requests
            if request.method == 'POST':
                for validate in validators:
                    try:
                        validate(request.form)  # Apply validation to form data
                    except ValidationError as e:
                        flash(str(e))
                        return redirect(url_for('home'))  # Redirect to homepage on error
            return f(*args, **kwargs)
        return decorated_function
    return decorator



# TODO determine if there is a reason to store the uploads rather than using them in memory
@input_validation_decorator(validate_students_df)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # check if the post request has the file part
        if "students" not in request.files or "projects" not in request.files:
            flash("Need both students and projects")
            return redirect(request.url)
        students = request.files["students"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if students.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if students and allowed_file(students.filename):
            #students_filename = secure_filename(students.filename)
            #students.save(os.path.join(app.config["UPLOAD_FOLDER"], students_filename))
            students_df = parse_df_upload(students)
            students_df = students_df.rename(
                columns={students_df.columns[0]: "student_names"}
            )
            #if not validate_students_df(students_df)[0]:
            #    flash(validate_students_df(students_df)[1])
            #    return redirect(request.url)
        projects = request.files["projects"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if projects.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if projects and allowed_file(projects.filename):
            #projects_filename = secure_filename(projects.filename)
            #projects.save(os.path.join(app.config["UPLOAD_FOLDER"], projects_filename))
            projects_df = parse_df_upload(projects)
            projects_df = projects_df.rename(
                columns={
                    projects_df.columns[0]: "project_names",
                    projects_df.columns[1]: "max_students",
                }
            )
            projects_df["max_students"] = pd.to_numeric(projects_df["max_students"])
            if not validate_projects_df(projects_df)[0]:
                flash(validate_projects_df(projects_df)[1])
                return redirect(request.url)
        if not validate_students_projects(students_df, projects_df)[0]:
            flash(validate_students_projects(students_df, projects_df)[1])
            return redirect(request.url)

        matches = pd.DataFrame.from_dict(
            matching_algorithm(students_df, projects_df), orient="index"
        )
        matches.reset_index(inplace=True)
        matches = matches.rename(
            columns={
                matches.columns[0]: "student_names",
                matches.columns[1]: "project_names",
            }
        )
        return render_template(
            "home.html",
            students=students_df.to_html(classes="table table-bordered", index=False),
            projects=projects_df.to_html(classes="table table-bordered", index=False),
            matches=matches.to_html(classes="table table-bordered", index=False),
        )

    # if not POST, render an empty version of the homepage so the user can upload students and projects
    else:
        return render_template("home.html", students="", projects="", matches="")
