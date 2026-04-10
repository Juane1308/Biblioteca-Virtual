from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from modelos.libro import Libro
from modelos.prestamo import Prestamo

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')


@usuario_bp.route('/catalogo')
@login_required
def catalogo():
    query      = request.args.get('q', '').strip()
    genero_act = request.args.get('genero', '').strip()

    if query:
        libros = Libro.buscar(query)
    else:
        libros = Libro.listar_todos()

    if genero_act:
        libros = [l for l in libros if l.genero == genero_act]

    # Géneros únicos para los filtros
    todos = Libro.listar_todos()
    generos = sorted({l.genero for l in todos if l.genero})

    return render_template(
        'usuario/catalogo.html',
        libros=libros,
        query=query,
        generos=generos,
        genero_activo=genero_act
    )


@usuario_bp.route('/detalle/<int:libro_id>')
@login_required
def detalle(libro_id):
    libro = Libro.buscar_por_id(libro_id)

    prestamo_activo = next(
        (p for p in current_user.prestamos if p.libro_id == libro_id and p.estado == 'Activo'),
        None
    )
    historial = Prestamo.historial_libro(libro_id) if current_user.es_admin else []

    return render_template(
        'usuario/detalle.html',
        libro=libro,
        prestamo_activo=prestamo_activo,
        historial=historial
    )


@usuario_bp.route('/detalle/<int:libro_id>/solicitar', methods=['POST'])
@login_required
def solicitar_prestamo(libro_id):
    libro = Libro.buscar_por_id(libro_id)
    _, error = Prestamo.registrar_prestamo(current_user, libro)
    if error:
        flash(error, 'danger')
    else:
        flash(f'Préstamo de "{libro.titulo}" registrado. Tienes 14 días.', 'success')
    return redirect(url_for('usuario.detalle', libro_id=libro_id))


@usuario_bp.route('/prestamo/<int:prestamo_id>/devolver', methods=['POST'])
@login_required
def devolver(prestamo_id):
    prestamo = Prestamo.buscar_por_id(prestamo_id)
    if prestamo.usuario_id != current_user.id and not current_user.es_admin:
        flash('No tienes permiso para esta acción.', 'danger')
        return redirect(url_for('usuario.mis_prestamos'))
    prestamo.registrar_devolucion()
    flash('Libro devuelto correctamente.', 'success')
    return redirect(url_for('usuario.mis_prestamos'))


@usuario_bp.route('/mis-prestamos')
@login_required
def mis_prestamos():
    prestamos = Prestamo.historial_usuario(current_user.id)
    return render_template('usuario/mis_prestamos.html', prestamos=prestamos)
