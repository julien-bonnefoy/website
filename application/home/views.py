# -*- coding: utf-8 -*-
""" HOME VIEWS

BLUEPRINT: home_np
ROUTES FUNCTIONS: index, home, register, login, logout, readme, contact, about, translate, search, send_message
OTHER FUNCTIONS: before_request
"""
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import login_required
from application.users.forms import SearchForm
from flask import Blueprint
from flask_login import logout_user, current_user
from application.translate import translate
from application.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from application.home.forms import ContactForm
from pygments.formatters.html import HtmlFormatter
import markdown
from markupsafe import Markup
from application.email_sender import send_password_reset_email
from flask_babel import _, get_locale
from application.extensions import db
from application.users.models import User


home_bp = Blueprint(
    "home_bp",
    __name__,
    template_folder='../templates/',
    static_folder="../static/"
)



@home_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())



@home_bp.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    return render_template("auth/login.html", form=LoginForm())


@home_bp.route('/clock', methods=['GET'])
def clock():
    return render_template('clock/clock.html', title='Clock Clock 24')


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


@home_bp.route("/readme")
def readme():
    with open("README.md", "r") as fp:
        formatter = HtmlFormatter(
            style="solarized-dark", full=True, cssclass="codehilite",
        )
        styles = f"<style>{formatter.get_style_defs()}</style>"
        html = (
            markdown.markdown(fp.read(), extensions=["codehilite", "fenced_code"])
            .replace(
                # Fix relative path for image(s) when rendering README.md on index page
                'src="application/',
                'src="',
            )
            .replace("codehilite", "codehilite p-2 mb-3 bg-dark")
        )
        return render_template(
            "home/readme.html", content=Markup(html), styles=Markup(styles)
        )


@home_bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify(
        {
            'text': translate(
                request.form['text'],
                request.form['source_language'],
                request.form['dest_language']
            )
        }
    )


@home_bp.route('/search')
@login_required
def search():
    return render_template('home/search.html', title='Search')


