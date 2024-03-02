import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import pandas as pd

UPLOAD_FOLDER = '../src/uploads'
# TODO add support for CSV
ALLOWED_EXTENSIONS = {'txt', 'xlsx'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NOTASECRETONLYUSEFORDEBUGGING'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_type(filename):
    return filename.rsplit('.', 1)[1].lower()


def txt_to_df(txt_file):
    txt_file.seek(0)
    file_contents = txt_file.read().decode('utf-8')
    file_contents = file_contents.splitlines()
    file_contents = [line.split(" ") for line in file_contents]
    file_contents = pd.DataFrame(file_contents)
    return file_contents


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'student_preferences' not in request.files or 'projects' not in request.files:
            flash('Need both student_preferences and projects')
            return redirect(request.url)
        student_preferences = request.files['student_preferences']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if student_preferences.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if student_preferences and allowed_file(student_preferences.filename):
            student_preferences_filename = secure_filename(student_preferences.filename)
            student_preferences.save(os.path.join(app.config['UPLOAD_FOLDER'], student_preferences_filename))
            if file_type(student_preferences.filename) == 'txt':
                student_preferencess_df = txt_to_df(student_preferences)
            if file_type(student_preferences.filename) == 'xlsx':
                student_preferencess_df = pd.read_excel(student_preferences)

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
            
        return render_template('home.html', student_preferences = student_preferencess_df, projects = projects_df)

    return render_template('home.html', student_preferences = '', projects = projects_df)