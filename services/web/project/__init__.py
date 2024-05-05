import os
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    render_template
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

def are_creds_good(user,pw):
    pass
    #look into db and find 

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    return render_template('root.html') 


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)

@app.route("/login", methods=["GET", "POST"])
def login():
    username=request.form.get("username")
    password=request.form.get("password")
    
    good_credentials = are_creds_good(username,password)
    
    if username is "":
        return render_template('login.html', bad_credentials=False)
    else:
        if not good_credentials:
            return render_template('login.html', bad_credentials=True)
        else:
            return render_template('login.html', bad_credentials=False)

    return render_template('login.html')

@app.route("/logout", methods=["GET", "POST"])
def logout():
    pass

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    pass

@app.route("/create_message", methods=["GET", "POST"])
def create_message():
    pass

@app.route("/search", methods=["GET", "POST"])
def search():
    pass
