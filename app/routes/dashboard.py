# app/routes/dashboard.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required,  current_user
from functools import wraps


dashboard_bp = Blueprint('dashboard', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Acceso denegado. Se requieren privilegios de administrador.', 'danger')
            return redirect(url_for('dashboard.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@dashboard_bp.route('/')
@login_required
def dashboard():
    print('Dashboard')
    return render_template('dashboard/dashboard.html')