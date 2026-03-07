from flask import Flask, render_template, g
import sqlite3


app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template('index.html')

# below will be the actual directories leading to the keepass file for cloud storage

@app.route("/keepass", methods=[GET])
def keepass_page():
    return render_template('keepass/keepassdb.html')

