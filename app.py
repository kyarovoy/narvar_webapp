from flask import Flask, render_template, request, flash
from wtforms import Form,TextField,SelectField,validators,StringField,SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

application = Flask(__name__)
application.config.from_object(__name__)
application.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176d'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/team.db'
db = SQLAlchemy(application)

class TeamMember(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=False, nullable=False)
  email = db.Column(db.String(80), unique=True, nullable=False)
  occupation_id = db.Column(db.Integer, db.ForeignKey('occupation.id'), nullable=False)
  occupation = db.relationship('Occupation', backref="team")

class Occupation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)

db.create_all()
# Initialize Occupation list
if db.session.query(Occupation).count() == 0:
  for occupation in ['Software Developer', 'QA', 'DevOps', 'CEO']:
    db.session.add(Occupation(name=occupation))
  db.session.commit()

class NarvarForm(Form):
  name = TextField('Name:', validators=[validators.required()])
  email = TextField('Email:', validators=[validators.required()])
  occupation = QuerySelectField('Occupation:', query_factory=lambda: db.session.query(Occupation), get_label='name')

@application.route("/webapp", methods=['GET','POST'])

def index():
    team = db.session.query(TeamMember).all()
    f = NarvarForm(request.form)
    print(f.errors)

    if request.method == 'POST':
      if f.validate():
        db.session.add(TeamMember(name=request.form['name'], email=request.form['email'], occupation_id=request.form['occupation']))
        try:
          db.session.commit()
          flash('Team member added')
        except exc.SQLAlchemyError:
          db.session.rollback()
          flash('SQL Error while inserting record to a database')
      else:
        flash('Form validation failure')

    return render_template('hello.html', form=f, users=team)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
