from flask import Flask, redirect, url_for, render_template
from modelos import db, bcrypt, login_manager
from controladores.auth import auth_bp
from controladores.usuario import usuario_bp
from controladores.admin import admin_bp


def create_app():
    app = Flask(__name__, template_folder='plantillas', static_folder='estatico')
    app.config['SECRET_KEY'] = 'mi_secreto_super_seguro_12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def not_found(_):
        return render_template('shared/404.html'), 404

    @app.errorhandler(403)
    def forbidden(_):
        return render_template('shared/403.html'), 403

    return app


def sembrar_datos(app):
    with app.app_context():
        from modelos.usuario import Usuario
        from modelos.libro import Libro
        from modelos.autor import Autor

        if not Usuario.buscar_por_username('admin'):
            admin = Usuario(username='admin', email='admin@biblioteca.local',
                            nombre='Administrador', rol='admin')
            admin.set_password('admin123')
            admin.guardar()
            print('admin / admin123')

        if not Usuario.buscar_por_username('usuario1'):
            user = Usuario(username='usuario1', email='usuario1@biblioteca.local',
                           nombre='Usuario de Prueba', rol='usuario')
            user.set_password('usuario123')
            user.guardar()
            print('usuario1 / usuario123')

        if Libro.query.count() == 0:
            autor1 = Autor(nombre='Gabriel García Márquez', nacionalidad='Colombiana')
            autor2 = Autor(nombre='Jorge Luis Borges', nacionalidad='Argentina')
            db.session.add_all([autor1, autor2])
            db.session.flush()

            libro1 = Libro(isbn='9780060883287', titulo='Cien años de soledad',
                           genero='Realismo mágico', anio_pub=1967,
                           descripcion='La historia de la familia Buendía a lo largo de siete generaciones.',
                           ejemplares_total=3, ejemplares_disponibles=3)
            libro1.autores.append(autor1)

            libro2 = Libro(isbn='9780142437247', titulo='Ficciones',
                           genero='Cuentos', anio_pub=1944,
                           descripcion='Colección de cuentos que exploran laberintos, espejos y el infinito.',
                           ejemplares_total=2, ejemplares_disponibles=2)
            libro2.autores.append(autor2)

            libro3 = Libro(isbn='9789584295154', titulo='El amor en los tiempos del cólera',
                           genero='Novela', anio_pub=1985,
                           descripcion='Historia de amor que persiste durante más de cincuenta años.',
                           ejemplares_total=2, ejemplares_disponibles=2)
            libro3.autores.append(autor1)

            db.session.add_all([libro1, libro2, libro3])
            db.session.commit()
            print('Libros y autores de ejemplo creados')


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        sembrar_datos(app)
    print('Servidor en http://localhost:5000')
    app.run(debug=True)
