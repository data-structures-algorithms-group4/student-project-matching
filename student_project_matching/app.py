import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from student_project_matching.matching_algorithm import matching_algorithm

# TODO find a better solution than manually going up one directory with "../"
UPLOAD_FOLDER = '../student_project_matching/uploads'
# TODO add support for CSV
ALLOWED_EXTENSIONS = {'txt', 'xlsx'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NOT-A-SECRET-ONLY-USE-FOR-LOCAL-TESTING'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def file_type(filename):
    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename):
    return file_type(filename) in ALLOWED_EXTENSIONS


def txt_to_df(txt_file):
    txt_file.seek(0)
    file_contents = txt_file.read().decode('utf-8')
    file_contents = file_contents.splitlines()
    file_contents = [line.split(" ") for line in file_contents]
    df = pd.DataFrame(file_contents)
    return df


# TODO determine if there is a reason to store the uploads rather than using them in memory
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'students' not in request.files or 'projects' not in request.files:
            flash('Need both students and projects')
            return redirect(request.url)
        students = request.files['students']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if students.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if students and allowed_file(students.filename):
            students_filename = secure_filename(students.filename)
            students.save(os.path.join(app.config['UPLOAD_FOLDER'], students_filename))
            if file_type(students.filename) == 'txt':
                students_df = txt_to_df(students)
            if file_type(students.filename) == 'xlsx':
                students_df = pd.read_excel(students)

        projects = request.files['projects']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if projects.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if projects and allowed_file(projects.filename):
            projects_filename = secure_filename(projects.filename)
            projects.save(os.path.join(app.config['UPLOAD_FOLDER'], projects_filename))
            if file_type(projects.filename) == 'txt':
                projects_df = txt_to_df(projects)
            if file_type(projects.filename) == 'xlsx':
                projects_df = pd.read_excel(projects)

        students_df = students_df.rename(columns = {students_df.columns[0]: 'student_names'})
        projects_df = projects_df.rename(columns = {projects_df.columns[0]: 'project_name', projects_df.columns[1]: 'max_students'})
        projects_df['max_students'] = pd.to_numeric(projects_df['max_students'])

        matches = pd.DataFrame.from_dict(matching_algorithm(students_df, projects_df), orient='index')
        matches.reset_index(inplace=True)
        matches = matches.rename(columns = {matches.columns[0]: 'student_names', matches.columns[1]: 'project_names'})
        return render_template('home.html',
                               students = students_df.to_html(classes="table table-bordered", index=False),
                               projects = projects_df.to_html(classes="table table-bordered", index=False),
                               matches = matches.to_html(classes="table table-bordered", index=False))
    
    # if not POST, render an empty version of the homepage so the user can upload students and projects
    else:
        return render_template('home.html', students = '', projects = '', matches = '')