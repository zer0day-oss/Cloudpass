from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from pykeepass import PyKeePass
import sqlite3
import subprocess

app = Flask(__name__)

dbpath = 'Cloudpass/server/keepass/keepass_creds.sqlite'
UPLOAD_FOLDER = 'Cloudpass/server/uploads'
ALLOWED_EXTENSIONS = {'csv', 'json', 'txt', 'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
s = subprocess

@app.route("/")
def index_page():
    return render_template('index.html')

# below will be the actual directories leading to the keepass file for cloud storage

@app.route("/dashboard", methods=['GET'])
def keepass_page():
    return render_template('keepassdb.html')

@app.route("/credentials")
def credentials_page():
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()


    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      site TEXT NULL,
                      username TEXT NULL,
                      email TEXT NULL,
                      password TEXT NOT NULL,
                      description TEXT NULL)''')
    
    conn.commit()
    conn.close()
    return render_template('credentials.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route("/upload_page")
def upload_page():
    return render_template('upload_form.html')

@app.route("/uploads", methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            return 'File uploaded successfully', render_template('upload_form.html')
        
    return 'File upload failed'

    
        

if __name__ == '__main__':
    app.run(debug=True)