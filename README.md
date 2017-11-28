# narvar_webappp

This is a demo web application written in Python 3.6 using Flask microframework. 
Goal of this application is to demonstrate how to perform common operations with webforms and interact with database.
Libraries used: Flask, SQLAlchemy, WTForms.

Application:
- displays contents of SQLite table "Team Members"
- displays a form, which allows to define Name, Email and Occupation (dropdown field pre-populated from a database)
- peforms basic validation of submitted form fields (all fields are required)
- if validation succeeded - information is stored in SQLite database on the server and a message is displayed
- if validation has failed or there is an SQL error - corresponding message is displayed

Install dependencies
```
pip install -r requirements.txt
```

Run application
```
python3.6 gunicorn wsgi
```
Once started application is available at /webapp URL.
