from flask import render_template, redirect, url_for, flash, request, Blueprint, current_app, g, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
from app.database import db
from app.home.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, ContactForm
from app.user.models import User, Message, Notification
from app.email_sender import send_password_reset_email
import markdown
import markdown.extensions.fenced_code
from pygments.formatters.html import HtmlFormatter
from markupsafe import Markup

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp',
    __name__,
    template_folder='../templates/',
    static_folder='../static/',
)


@home_bp.route("/", methods=["GET", "POST"])
@home_bp.route("/index", methods=["GET", "POST"])
def index():
    form = LoginForm()
    return render_template('home/index.html', title=_('Home'), form=form)


@home_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home/home.html")


@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('home_bp.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_bp.index')
        return redirect(next_page)
    return render_template('home/index.html', title=_('Sign In'), form=form)


@home_bp.route('/logout')
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return render_template("home/home.html")


@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered users!'))
        return redirect(url_for('home_bp.login'))
    return render_template('home/register.html', title=_('Register'),
                           form=form)


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
        return redirect(url_for('home_bp.login'))
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
        return redirect(url_for('home_bp.login'))
    return render_template('home/reset_password.html', form=form)


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
            style="solarizeddark", full=True, cssclass="codehilite",
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
            "index.html", content=Markup(html), styles=Markup(styles),
        )