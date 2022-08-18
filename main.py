import imp
import os
from flask import Flask, render_template, url_for, request, redirect
from flask.views import View, MethodView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# config Flask app
app = Flask(__name__)

# database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///akotodb.sqlite3"    # name of db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# create db instance
db = SQLAlchemy(app)


# Akoto Tuition page - name, email, date
class Tuition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(12))

    def __init__(self, first_name, last_name, email, date):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date = date

# Contact me page - name, email, interest (collaboration, development, tuition, other), date, message
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    interst = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(12))
    message = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, interest, date, message):
        self.name = name
        self.email = email
        self.interst = interest
        self.date = date
        self.message = message


"""create app class views"""
# homepage (about me etc)
class Home(View):
    def dispatch_request(self):
        return render_template("homepage.html")

# akoto tech tuition (courses, price, leave details of interest)
class AkotoTuition(MethodView):
    def get(self):
        return render_template("akototuition.html")
    
    def post(self):
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("customer_email")
        date = datetime.strftime(datetime.today(), "%d %b %Y")
        # adding the data to a database
        create_data = Tuition(first_name=first_name, last_name=last_name, email=email, date=date)
        db.session.add(create_data)
        db.session.commit()
        # getting data back out to display
        get_data = Tuition.query.filter_by(email=email).first()    # filter user by users' email
        print(get_data.first_name)
        return render_template("akototuition.html", first_name=first_name, last_name=last_name, email=email, date=date, get_data=get_data)

# references (cv to download, images of places worked)
class References(View):
    def dispatch_request(self):
        return render_template("references.html")

# projects (page to host projects)
# contact me (user contact page)

app.add_url_rule("/", view_func=Home.as_view(name="homepage"))
app.add_url_rule("/akototuition", view_func=AkotoTuition.as_view(name="akoto_tuition"))
app.add_url_rule("/references", view_func=References.as_view(name="ref"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
