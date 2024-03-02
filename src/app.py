import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import pandas as pd

UPLOAD_FOLDER = '../src/uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_type(filename):
    return filename.rsplit('.', 1)[1].lower()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if file_type(file.filename) == 'txt':
                file.seek(0)
                file_contents = file.read()
                print(f'File: {file}')
                print(f'File contents: {file_contents}')
                return render_template('home.html', student_preferences = file_contents)
            if file_type(file.filename) == 'xlsx':
                preferences_df = pd.read_excel(file)
                return render_template('home.html', student_preferences = preferences_df)

    return render_template('home.html', student_preferences = '')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)