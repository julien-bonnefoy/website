    # -*- coding: utf-8 -*-
""" USER VIEWS

BLUEPRINT: dash_bp
ROUTES FUNCTIONS: user, user_popup, edit_profile, messages, notifications, members
OTHER FUNCTIONS: load_user, before_request
"""
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app, Blueprint
from flask_login import login_required, current_user
from application.extensions import lm, db
from application.users.models import User
from datetime import datetime
from application.users.forms import SearchForm, EditProfileForm, EmptyForm,  MessageForm


user_bp = Blueprint(
    "user_bp", __name__,
    template_folder='/templates',
    static_folder="/static",
    url_prefix='/users'
)


@lm.user_loader
def load_user(user_id):
    """Load users by ID."""
    return User.query.get(int(user_id))


@user_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@user_bp.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('users/user.html', user=user, form=form)


@user_bp.route('/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('users/user_popup.html', user=user, form=form)


@user_bp.route('/<username>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('home_bp.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', title='Edit Profile', form=form)


@user_bp.route("/members")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")
