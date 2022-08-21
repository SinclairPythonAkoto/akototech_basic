# Basic Skeleton Akoto Tech App #

This will be a basic Flask app of my Akoto Tech web app.

The aim of this web app is to produce a basic skeleton of my web app and create the app routes using class based views.

**Required Installations**
```
pip install Flask
pip install flask-sqlalchemy
pip install datetime
```

**Environment Variable**
I used *environment variables* to keep sensitive data like my login details private.  The environment variable was created on my terminal then used the `os` library to use the same variable within my Python script.
```
# create environmant variable in Windows PowerShell
$env:VARIABLE_NAME = 'Environment varibale value'

# use EV in script
os.environ.get('VARIABLE_NAME')
os.environ['VARIABLE_NAME']
```

**Run app**
```
python main.py
```