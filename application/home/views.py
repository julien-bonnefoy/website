# -*- coding: utf-8 -*-
""" HOME VIEWS

BLUEPRINT: home_np
ROUTES FUNCTIONS: index, home, register, login, logout, readme, contact, about, translate, search, send_message
OTHER FUNCTIONS: before_request
"""
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import login_required
from application.users.forms import SearchForm, EmptyForm
from flask import Blueprint
from flask_login import logout_user, current_user
from application.translate import translate
from application.auth.forms import LoginForm, ResetPasswordRequestForm
from application.home.forms import ContactForm
from pygments.formatters.html import HtmlFormatter
import markdown
from markupsafe import Markup
from application.email_sender import send_password_reset_email
from application.extensions import db
from application.users.models import User


home_bp = Blueprint(
    "home_bp",
    __name__,
    template_folder='../../templates/',
    static_folder="../../static/"
)


@home_bp.route('/index', methods=['GET', 'POST'])
@home_bp.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('home_bp.home'))
    return render_template("home/index.html", form=LoginForm())


@home_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home/home.html")


@home_bp.route("/about")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("home/about.html", form=form)


@home_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Standard `contact` form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "home/contact.html",
        form=form
    )


