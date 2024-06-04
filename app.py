# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = '0611758376'  # Replace with a strong secret key

# Database configuration (replace with your actual database setup)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # Store passwords as plain text (INSECURE)
    perimeter = db.Column(db.String(50))
    dataiku_api_key = db.Column(db.String(255))

with app.app_context():
    db.create_all() 

class RegistrationForm(FlaskForm):
    matricule = StringField('Matricule', validators=[DataRequired()])
    perimeter = SelectField('Périmètre', choices=[('p1', 'Périmètre 1'), ('p2', 'Périmètre 2'), ('p3', 'Périmètre 3')])
    dataiku_api_key = StringField('API Key Dataiku Personnel', validators=[DataRequired()], 
                                  render_kw={"placeholder": "Enter your Dataiku API Key"})
    password = PasswordField('Mot de passe', validators=[DataRequired(), EqualTo('confirm_password', message='Les mots de passe ne correspondent pas.')])
    confirm_password = PasswordField('Confirmation de mot de passe', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class LoginForm(FlaskForm):
    matricule = StringField('Matricule', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(matricule=form.matricule.data, 
                        perimeter=form.perimeter.data, 
                        dataiku_api_key=form.dataiku_api_key.data, 
                        password=form.password.data) # Store password directly (INSECURE)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('auth.html', form=form, is_register=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(matricule=form.matricule.data).first()
        if user and user.password == form.password.data: # Direct password comparison (INSECURE)
            return redirect(url_for('home'))  # Replace with your home page route
        else:
            return 'Invalid matricule or password'
    return render_template('auth.html', form=form)

@app.route('/traduc')
def home():
    # Protect this route with authentication (e.g., using Flask-Login)
    return 'Authentification réussie'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8112)