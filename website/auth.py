from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Check Password', validators=[DataRequired()])

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = form.email.data
            password = form.password.data
            print('hello')
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category="success")
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect Password', category='error')
            else:
                flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user, form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = form.email.data
            first_name = form.first_name.data
            password1 = form.password1.data
            password2 = form.password2.data

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Emal already exists', category="error")
            elif len(email) < 4:
                flash("Email must be greater than 3 characters.", category='error')
            elif len(first_name) < 2:
                flash("First Name must be greater than 1 characters.", category='error')
            elif password1 != password2:
                flash("Passwords don't match.", category='error')
            elif len(password1) < 7:
                flash("Password must be at least 7 characters.", category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("Account created!", category="success")
                return redirect(url_for('views.home'))
    return render_template("sign_up.html", form=form)
