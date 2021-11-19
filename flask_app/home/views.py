# -*- coding: utf-8 -*-
""" HOME VIEWS

BLUEPRINT: home_np
ROUTES FUNCTIONS: index, home, register, login, logout, readme, contact, about, translate, search, send_message
OTHER FUNCTIONS: before_request
"""
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import login_required
from flask_app import db
from werkzeug.urls import url_parse
from flask_app.users.forms import SearchForm
from flask import Blueprint
from flask_login import login_user, logout_user, current_user
from flask_app.translate import translate
from flask_app.home.forms import LoginForm, RegistrationForm, ContactForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_app.users.models import User
from pygments.formatters.html import HtmlFormatter
import markdown
from markupsafe import Markup
from flask_app.email_sender import send_password_reset_email
from flask_babel import _, get_locale

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



@home_bp.route('/', methods=['GET', 'POST'])
@home_bp.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    return render_template('home/index.html', title='Landing Page')


@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('home_bp.index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_bp.home')
        return redirect(next_page)
    return render_template('home/login2.html', title=_('Sign In'), form=form)


@home_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', "success")
        return redirect(url_for('home_bp.login'))
    return render_template('home/register.html', title='Register', form=form)


@home_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home/home.html")



@home_bp.route("/logout")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for('home_bp.index'))




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
                'src="app/',
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
    return render_template('home/search.html', title=_('Search'))




@home_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('home/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@home_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('home/reset_password.html', form=form)

