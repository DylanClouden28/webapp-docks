from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Check Password', validators=[DataRequired()])

class BoatLogForm(FlaskForm):
    boat_reg = StringField('Boat Registration')
    boat_name = StringField('Boat Name')
    boat_size = RadioField('Boat Size', choices=[('0-25','25 feet and Under'), ('26-40', '26 feet to 40'), ('41-Over', '41 feet and over') ] , validators=[DataRequired()])
    owner_name = StringField('Owner\'s Name')
    phone_number = StringField('Phone Number')
    email = StringField('Email')
    zipcode = StringField('Zipcode or Postal Code')
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    boat_reg = StringField('Search Boat Registration')
    boat_name = StringField('Search Boat Name')
    phone_number = StringField('Search Phone Number')
    submit = SubmitField('Submit')
