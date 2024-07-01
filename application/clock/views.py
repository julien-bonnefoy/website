# -*- coding: utf-8 -*-
""" CLOCK VIEWS

BLUEPRINT: clock_bp
ROUTES FUNCTIONS: clock
OTHER FUNCTIONS:
"""
from flask import Blueprint, render_template

# Blueprint Configuration
clock_bp = Blueprint(
    'clock_bp',
    __name__,
    template_folder='../templates/',
    static_folder='../static/'
)

@clock_bp.route('/clock', methods=['GET'])
def clock():
    return render_template('clock/clock.html', title='Clock Clock 24')
