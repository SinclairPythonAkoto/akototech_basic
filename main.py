from flask import Flask, render_template
from flask.views import View, MethodView
from flask_sqlalchemy import SQLAlchemy

# config Flask app
app = Flask(__name__)

# database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///akotodb.sqlite3"    # name of db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# create db instance
db = SQLAlchemy(app)

"""create the database tables"""
# Akoto Tuition page - name, email, date
class Tuition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime)

    def __init__(self, name, email, date):
        self.name = name
        self.email = email
        self.date = date

# Contact me page - name, email, interest (collaboration, development, tuition, other), date, message
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    interst = db.Column(db.String(15), nullable=False)
    date = db.Column(db.DateTime)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, interest, date, message):
        self.name = name
        self.email = email
        self.interst = interest
        self.date = date
        self.message = message



"""create app class views"""
# homepage (about me etc)
# akoto tech tuition (courses, price, leave details of interest)
# references (cv to download, images of places worked)
# projects (page to host projects)
# contact me (user contact page)

@app.route("/")
def home():
    return render_template("homepage.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
