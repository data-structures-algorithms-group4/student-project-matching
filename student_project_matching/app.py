import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_file,
    send_from_directory,
    session,
    render_template,
)
from werkzeug.utils import secure_filename
import pandas as pd
from student_project_matching.matching_algorithm import matching_algorithm
from student_project_matching.input_validation import validate_students_df, validate_projects_df, validate_students_projects
import io

# TODO find a better solution than manually going up one directory with "../"
UPLOAD_FOLDER = "../student_project_matching/uploads"
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


def parse_df_upload(file):
    if file_type(file.filename) == "txt":
        df = txt_to_df(file)
    if file_type(file.filename) == "xlsx":
        df = pd.read_excel(file)
    if file_type(file.filename) == "csv":
        file.seek(0)
        df = pd.read_csv(file, header=0)
    return df


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # check if the post request has the file part
        if "students" not in request.files or "projects" not in request.files:
            flash("Need both students and projects")
            return redirect(request.url)
        students = request.files["students"]
        projects = request.files["projects"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if students.filename == "":
            flash("No students file")
            return redirect(request.url)
        if projects.filename == "":
            flash("No projects file")
            return redirect(request.url)
        if not allowed_file(students.filename):
            flash("Students file must be XLSX, CSV, or TXT")
            return redirect(request.url)
        if not allowed_file(projects.filename):
            flash("Projects file must be XLSX, CSV, or TXT")
            return redirect(request.url)
        students_df = parse_df_upload(students)
        students_df = students_df.rename(
            columns={students_df.columns[0]: "student_names"}
        )
        success, error_message = validate_students_df(students_df)
        if not success:
            flash(error_message)
            return redirect(request.url)
        projects_df = parse_df_upload(projects)
        projects_df = projects_df.rename(
            columns={
                projects_df.columns[0]: "project_names",
                projects_df.columns[1]: "max_students",
            }
        )
        projects_df["max_students"] = pd.to_numeric(projects_df["max_students"])
        success, error_message = validate_projects_df(projects_df)
        if not success:
            flash(error_message)
            return redirect(request.url)
        success, error_message = validate_students_projects(students_df, projects_df)
        if not success:
            flash(error_message)
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
        session["matches"] = matches.to_json(date_format='iso', orient='split')
        return render_template(
            "home.html",
            students=students_df.to_html(classes="table table-bordered", index=False),
            projects=projects_df.to_html(classes="table table-bordered", index=False),
            matches=matches.to_html(classes="table table-bordered", index=False),
        )

    # if not POST, render an empty version of the homepage so the user can upload students and projects
    else:
        return render_template("home.html", students="", projects="", matches="")


@app.route("/download-matches", methods = ["GET"])
def download_matches():
    json_matches = session.get("matches")
    if json_matches:
        matches = pd.read_json(json_matches, orient='split')
        matches_csv = io.BytesIO()
        matches.to_csv(matches_csv, index=False, encoding='utf-8')
        matches_csv.seek(0)
        return send_file(
            matches_csv,
            mimetype='text/csv',
            as_attachment=True,
            download_name='student-project-matches.csv'
        )
    else:
        render_template("home.html", students="", projects="", matches="")