from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from modelos.usuario import Usuario

auth_bp = Blueprint('auth', __name__)


def _sin_cache(response):
    resp = make_response(response)
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    return resp


def _redirigir_por_rol(usuario):
    if usuario.es_admin:
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.inicio'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return _redirigir_por_rol(current_user)

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Completa todos los campos.', 'danger')
            return _sin_cache(render_template('login.html'))

        usuario = Usuario.buscar_por_username(username) or Usuario.buscar_por_email(username)

        if not usuario or not usuario.check_password(password):
            flash('Usuario o contraseña incorrectos.', 'danger')
            return _sin_cache(render_template('login.html'))

        if not usuario.activo:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
            return _sin_cache(render_template('login.html'))

        login_user(usuario)
        return _redirigir_por_rol(usuario)

    return _sin_cache(render_template('login.html'))


@auth_bp.route('/registro', methods=['POST'])
def registro():
    username = request.form.get('username', '').strip()
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    nombre   = request.form.get('nombre', '').strip() or username

    if not all([username, email, password]):
        flash('Usuario, email y contraseña son obligatorios.', 'danger')
        return redirect(url_for('auth.login'))

    if Usuario.buscar_por_username(username):
        flash('Ese nombre de usuario ya está en uso.', 'danger')
        return redirect(url_for('auth.login'))

    if Usuario.buscar_por_email(email):
        flash('Ese email ya está registrado.', 'danger')
        return redirect(url_for('auth.login'))

    nuevo = Usuario(username=username, email=email, nombre=nombre, rol='usuario')
    nuevo.set_password(password)
    nuevo.guardar()

    login_user(nuevo)
    flash('¡Cuenta creada! Bienvenido/a.', 'success')
    return redirect(url_for('auth.inicio'))


@auth_bp.route('/inicio')
@login_required
def inicio():
    return render_template('inicio.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
