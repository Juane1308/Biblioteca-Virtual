from flask import Flask, redirect, url_for
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

    with app.app_context():
        from modelos.usuario import Usuario
        from modelos.prestamo import Prestamo
        from modelos.libro import Libro
        from modelos.autor import Autor
        db.create_all()

        if not Usuario.buscar_por_username('admin'):
            admin = Usuario(
                username='admin',
                email='admin@biblioteca.local',
                nombre='Administrador',
                rol='admin'
            )
            admin.set_password('admin123')
            admin.guardar()

        if not Usuario.buscar_por_username('usuario1'):
            usuario = Usuario(
                username='usuario1',
                email='usuario1@biblioteca.local',
                nombre='Usuario de Prueba',
                rol='usuario'
            )
            usuario.set_password('usuario123')
            usuario.guardar()

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

