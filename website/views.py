from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from flask_login import login_required

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html")

@views.route('/boatlog')
@login_required
def boatlog():
    return render_template("boatlog.html")