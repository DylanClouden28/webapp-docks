from wtforms import StringField, PasswordField, RadioField, SubmitField, HiddenField
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

class PaymentForm(FlaskForm):
    selectedRowId = HiddenField("Feild 1")
    date_in = StringField('Date In', validators=[DataRequired()])
    date_paid = StringField('Date Paid', validators=[DataRequired()])
    paid_days = StringField('Paid Days', validators=[DataRequired()])
    paid_nights = StringField('Paid Nights', validators=[DataRequired()])
    unpaid_days = StringField('Unpaid Days')
    unpaid_nights = StringField('Unpaid Nights')
    paid_enw = RadioField('Electric / Water', choices=[('Yes','Yes'), ('No', 'No') ] , validators=[DataRequired()])
    paid_with  = RadioField('Payment Method', choices=[('Cash','Cash'), ('Check', 'Check'), ('Charge', 'Charge') ] , validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteVisitForm(FlaskForm):
    selecteddeleteRowId = HiddenField("Field 1")

class SearchForm(FlaskForm):
    boat_reg = StringField('Search Boat Registration')
    boat_name = StringField('Search Boat Name')
    phone_number = StringField('Search Phone Number')
    submit = SubmitField('Submit')

class PaymentForm(FlaskForm):
    selectedRowId = HiddenField("Feild 1")
    date_in = StringField('Date In', validators=[DataRequired()])
    date_paid = StringField('Date Paid', validators=[DataRequired()])
    paid_days = StringField('Paid Days', validators=[DataRequired()])
    paid_nights = StringField('Paid Nights', validators=[DataRequired()])
    unpaid_days = StringField('Unpaid Days')
    unpaid_nights = StringField('Unpaid Nights')
    paid_enw = RadioField('Electric / Water', choices=[('Yes','Yes'), ('No', 'No') ] , validators=[DataRequired()])
    paid_with  = RadioField('Payment Method', choices=[('Cash','Cash'), ('Check', 'Check'), ('Charge', 'Charge') ] , validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteVisitForm(FlaskForm):
    selecteddeleteRowId = HiddenField("Field 1")

class SearchForm(FlaskForm):
    boat_reg = StringField('Search Boat Registration')
    boat_name = StringField('Search Boat Name')
    phone_number = StringField('Search Phone Number')
    submit = SubmitField('Submit')

class PhoneNumber(FlaskForm):
    phone_number = StringField('Phone Number')
    submit = SubmitField('Submit')

class PublicLogin(FlaskForm):
    boat_reg = StringField('Boat Registration')
    boat_name = StringField('Boat Name (Leave blank if no name)')
    boat_size = RadioField('Boat Size', choices=[('0-25','25 ft and Under'), ('26-40', '26 ft to 40'), ('41-Over', '41 ft and over') ] , validators=[DataRequired()])
    owner_name = StringField('Name of boat owner', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    zipcode = StringField('Zipcode or Postal Code', validators=[DataRequired()])
    total_nights = RadioField('Total nights', choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[DataRequired()])
    day_fee = RadioField('Day fee', choices=[(1, 'Yes'), (0, 'No')], validators=[DataRequired()])
    water_electric = RadioField('Will you be using water or electric', choices=[(0, 'Yes'), (1, 'No')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class PublicPay(FlaskForm):
    total_nights = RadioField('Total nights', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[DataRequired()])
    day_fee = RadioField('Day fee', choices=[(0, 'Yes'), (1, 'No')], validators=[DataRequired()])
    water_electric = RadioField('Will you be using water or electric', choices=[(0, 'Yes'), (1, 'No')], validators=[DataRequired()])