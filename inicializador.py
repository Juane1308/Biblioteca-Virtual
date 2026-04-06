from flask import Flask, redirect, url_for
from modelos import db, bcrypt, login_manager
from controladores.auth import auth_bp

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

    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
