from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from modelos import db
from modelos.libro import Libro
from modelos.autor import Autor
from modelos.usuario import Usuario
from modelos.prestamo import Prestamo
from datetime import date

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def solo_admin(fn):
    """Decorador: aborta con 403 si el usuario no es admin."""
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

@admin_bp.route('/')
@login_required
@solo_admin
def dashboard():
    total_libros     = Libro.query.count()
    total_usuarios   = Usuario.query.count()
    prestamos_activos = Prestamo.query.filter_by(estado='Activo').count()
    todos_activos    = Prestamo.query.filter_by(estado='Activo').all()
    prestamos_vencidos = sum(1 for p in todos_activos if p.esta_vencido())
    prestamos_recientes = (Prestamo.query
                           .order_by(Prestamo.fecha_prestamo.desc())
                           .limit(10).all())
    return render_template('admin/dashboard.html',
                           total_libros=total_libros,
                           total_usuarios=total_usuarios,
                           prestamos_activos=prestamos_activos,
                           prestamos_vencidos=prestamos_vencidos,
                           prestamos_recientes=prestamos_recientes)


# ─────────────────────────────────────────────
# LIBROS
# ─────────────────────────────────────────────

@admin_bp.route('/libros')
@login_required
@solo_admin
def libros():
    query = request.args.get('q', '').strip()
    libros = Libro.buscar(query) if query else Libro.listar_todos()
    return render_template('admin/libros.html', libros=libros, query=query)


@admin_bp.route('/libros/crear', methods=['POST'])
@login_required
@solo_admin
def crear_libro():
    isbn       = request.form.get('isbn', '').strip()
    titulo     = request.form.get('titulo', '').strip()
    genero     = request.form.get('genero', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    anio_str   = request.form.get('anio_pub', '').strip()
    ejemplares = int(request.form.get('ejemplares_total', 1))
    autores_raw = request.form.get('autores_ids', '').strip()

    if not isbn or not titulo:
        flash('ISBN y título son obligatorios.', 'danger')
        return redirect(url_for('admin.libros'))

    if Libro.buscar_por_isbn(isbn):
        flash(f'Ya existe un libro con ISBN {isbn}.', 'danger')
        return redirect(url_for('admin.libros'))

    libro = Libro(
        isbn=isbn,
        titulo=titulo,
        genero=genero or None,
        descripcion=descripcion or None,
        anio_pub=int(anio_str) if anio_str.isdigit() else None,
        ejemplares_total=ejemplares,
        ejemplares_disponibles=ejemplares
    )

    if autores_raw:
        for aid in autores_raw.split(','):
            aid = aid.strip()
            if aid.isdigit():
                autor = Autor.query.get(int(aid))
                if autor:
                    libro.autores.append(autor)

    libro.guardar()
    flash(f'Libro "{titulo}" creado correctamente.', 'success')
    return redirect(url_for('admin.libros'))


@admin_bp.route('/libros/<int:libro_id>/editar', methods=['POST'])
@login_required
@solo_admin
def editar_libro(libro_id):
    libro = Libro.buscar_por_id(libro_id)
    libro.isbn        = request.form.get('isbn', libro.isbn).strip()
    libro.titulo      = request.form.get('titulo', libro.titulo).strip()
    libro.genero      = request.form.get('genero', '').strip() or None
    libro.descripcion = request.form.get('descripcion', '').strip() or None
    anio_str          = request.form.get('anio_pub', '').strip()
    libro.anio_pub    = int(anio_str) if anio_str.isdigit() else None
    nuevos_ejemplares = int(request.form.get('ejemplares_total', libro.ejemplares_total))
    diff = nuevos_ejemplares - libro.ejemplares_total
    libro.ejemplares_total = nuevos_ejemplares
    libro.ejemplares_disponibles = max(0, libro.ejemplares_disponibles + diff)
    db.session.commit()
    flash(f'Libro "{libro.titulo}" actualizado.', 'success')
    return redirect(url_for('admin.libros'))


@admin_bp.route('/libros/<int:libro_id>/eliminar', methods=['POST'])
@login_required
@solo_admin
def eliminar_libro(libro_id):
    libro = Libro.buscar_por_id(libro_id)
    titulo = libro.titulo
    libro.eliminar()
    flash(f'Libro "{titulo}" eliminado.', 'success')
    return redirect(url_for('admin.libros'))


# ─────────────────────────────────────────────
# USUARIOS
# ─────────────────────────────────────────────

@admin_bp.route('/usuarios')
@login_required
@solo_admin
def usuarios():
    filtro_rol    = request.args.get('rol', '').strip()
    filtro_activo = request.args.get('activo', '').strip()

    query = Usuario.query
    if filtro_rol:
        query = query.filter_by(rol=filtro_rol)
    if filtro_activo == 'false':
        query = query.filter_by(activo=False)

    usuarios = query.order_by(Usuario.nombre).all()
    return render_template('admin/usuarios.html',
                           usuarios=usuarios,
                           filtro_rol=filtro_rol,
                           filtro_activo=filtro_activo)


@admin_bp.route('/usuarios/<int:usuario_id>/desactivar', methods=['POST'])
@login_required
@solo_admin
def desactivar_usuario(usuario_id):
    usuario = Usuario.buscar_por_id(usuario_id)
    if usuario.id == current_user.id:
        flash('No puedes desactivarte a ti mismo.', 'danger')
    else:
        usuario.desactivar()
        flash(f'Usuario "{usuario.username}" desactivado.', 'success')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/<int:usuario_id>/activar', methods=['POST'])
@login_required
@solo_admin
def activar_usuario(usuario_id):
    usuario = Usuario.buscar_por_id(usuario_id)
    usuario.activo = True
    db.session.commit()
    flash(f'Usuario "{usuario.username}" activado.', 'success')
    return redirect(url_for('admin.usuarios'))


# ─────────────────────────────────────────────
# PRÉSTAMOS
# ─────────────────────────────────────────────

@admin_bp.route('/prestamos')
@login_required
@solo_admin
def prestamos():
    filtro_estado   = request.args.get('estado', '').strip()
    filtro_vencidos = request.args.get('vencidos', '').strip()

    query = Prestamo.query.order_by(Prestamo.fecha_prestamo.desc())
    if filtro_estado:
        query = query.filter_by(estado=filtro_estado)

    prestamos = query.all()

    if filtro_vencidos:
        prestamos = [p for p in prestamos if p.esta_vencido()]

    return render_template('admin/prestamos.html',
                           prestamos=prestamos,
                           filtro_estado=filtro_estado,
                           filtro_vencidos=filtro_vencidos)


@admin_bp.route('/prestamos/crear', methods=['POST'])
@login_required
@solo_admin
def crear_prestamo():
    usuario_id = request.form.get('usuario_id', type=int)
    libro_id   = request.form.get('libro_id', type=int)

    usuario = Usuario.query.get(usuario_id)
    libro   = Libro.query.get(libro_id)

    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin.prestamos'))
    if not libro:
        flash('Libro no encontrado.', 'danger')
        return redirect(url_for('admin.prestamos'))

    _, error = Prestamo.registrar_prestamo(usuario, libro)
    if error:
        flash(error, 'danger')
    else:
        flash(f'Préstamo de "{libro.titulo}" registrado para {usuario.nombre}.', 'success')
    return redirect(url_for('admin.prestamos'))


@admin_bp.route('/prestamos/<int:prestamo_id>/devolver', methods=['POST'])
@login_required
@solo_admin
def registrar_devolucion(prestamo_id):
    prestamo = Prestamo.buscar_por_id(prestamo_id)
    prestamo.registrar_devolucion()
    flash('Devolución registrada correctamente.', 'success')
    return redirect(url_for('admin.prestamos'))
