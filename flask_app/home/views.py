# -*- coding: utf-8 -*-
""" HOME VIEWS

BLUEPRINT: home_np
ROUTES FUNCTIONS: index, home, register, logout, readme, contact, about, translate, search, send_message
OTHER FUNCTIONS: before_request
"""
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from flask_app import db
from flask_app.user.forms import SearchForm, MessageForm
from flask_app.user.models import User, Message
from flask import Blueprint
from flask_login import logout_user
from flask_app.translate import translate
from flask_app.home.forms import LoginForm, RegistrationForm, ContactForm
from flask_app.user.models import User
from flask_app.utils import flash_errors
from pygments.formatters.html import HtmlFormatter
import markdown
from markupsafe import Markup
from datetime import datetime

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
@login_required
def index():
    form = LoginForm
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate( page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template(
        'index.html',
        title=_('Home'),
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@home_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home/home.html")


@home_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("home_bp.home"))
    else:
        flash_errors(form)
    return render_template("home/register.html", form=form)


@home_bp.route("/logout")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
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


@home_bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('home/send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)

