# app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app.models.user import User


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_user_by_email(email)

        if user:
            print(user.email)
            print(user.username)

            if user.verify_password(password):
                login_user(user)
                flash('Inicio de sesión exitoso.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta.', 'danger')
        else:
            flash('Correo electrónico no encontrado.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    try:
        # Verificar si ya existe el admin
        if not User.objects(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@carpinteria.com',
                is_admin=True
            )
            admin_user.set_password('admin123')  # Contraseña temporal
            admin_user.save()
            flash('Usuario admin creado exitosamente!', 'success')
        else:
            flash('El usuario admin ya existe', 'warning')
    except Exception as e:
        flash(f'Error creando usuario: {str(e)}', 'danger')
    
    return redirect(url_for('auth.login'))  # Redirige al login