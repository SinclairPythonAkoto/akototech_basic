import os
from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask.views import View, MethodView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

# config Flask app
app = Flask(__name__)

# set session for secret key
app.secret_key = "Bond18SINclair60!RoBoTIcs?P91YthOn"

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

# Contact me page - name, email, reason (collaboration, development, tuition, other), date, message
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reason = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(12))

    def __init__(self, first_name, last_name, email, reason, date, message):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.reason = reason
        self.date = date
        self.message = message

# redirect to login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to sign in first')
            return redirect(url_for('admin_login'))
    return wrap

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
        return render_template("akototuition.html", first_name=first_name, last_name=last_name, email=email, date=date, get_data=get_data)

# references (cv to download, images of places worked)
class References(View):
    def dispatch_request(self):
        return render_template("references.html")

# projects (page to host projects)
class Projects(View):
    def dispatch_request(self):
        return render_template("projects.html")

# contact me (user contact page)
class ContactMe(MethodView):
    def get(self):
        return render_template("contact.html")
    
    def post(self):
        print(request.form)
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['userEmail']
        interest = request.form['interest']
        content = request.form['textContent']
        date = datetime.strftime(datetime.today(), "%d %b %Y")
        # add user info to Contact table
        create_data = Contact(first_name=first_name, last_name=last_name, email=email, reason=interest, message=content, date=date)
        db.session.add(create_data)
        db.session.commit()
        return redirect(url_for('homepage'))

class Login(MethodView):
    def get(self):
        return render_template("adminlogin.html")

    def post(self):
        username = request.form['username']
        password = request.form['userpass']
        if username == os.environ['USERNAME'] and password == os.environ['PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for("mypage"))
        return redirect(url_for('homepage'))

class AkotoTechApi(MethodView):
    @login_required
    def get(self, get_data):
        if get_data:
            return "Get data from database"
        else:
            return "My API page. Give instructions on how to query the database by using my API."

app.add_url_rule("/", view_func=Home.as_view(name="homepage"))
app.add_url_rule("/akototuition", view_func=AkotoTuition.as_view(name="akoto_tuition"))
app.add_url_rule("/references", view_func=References.as_view(name="ref"))
app.add_url_rule("/projects", view_func=Projects.as_view(name="projects"))
app.add_url_rule("/contact", view_func=ContactMe.as_view(name="contact"))
app.add_url_rule("/login", view_func=Login.as_view(name="admin_login"))
app.add_url_rule("/api/", defaults={'get_data': None}, view_func=AkotoTechApi.as_view(name="mypage"), methods=['GET'])

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
