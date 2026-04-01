from modelos import db
from modelos.autor import libro_autor


class Libro(db.Model):
    """Libro del catálogo bibliográfico."""
    __tablename__ = 'libro'

    id                      = db.Column(db.Integer, primary_key=True)
    isbn                    = db.Column(db.String(13), unique=True, nullable=False)
    titulo                  = db.Column(db.String(200), nullable=False)
    anio_pub                = db.Column(db.Integer, nullable=True)
    genero                  = db.Column(db.String(100), nullable=True)
    descripcion             = db.Column(db.Text, nullable=True)
    ejemplares_total        = db.Column(db.Integer, nullable=False, default=1)
    ejemplares_disponibles  = db.Column(db.Integer, nullable=False, default=1)

    autores  = db.relationship('Autor', secondary=libro_autor, back_populates='libros')
    prestamos = db.relationship('Prestamo', back_populates='libro', lazy=True)

    def esta_disponible(self):
        return self.ejemplares_disponibles > 0

    def reducir_disponibilidad(self):
        if self.ejemplares_disponibles > 0:
            self.ejemplares_disponibles -= 1
            db.session.commit()
            return True
        return False

    def aumentar_disponibilidad(self):
        if self.ejemplares_disponibles < self.ejemplares_total:
            self.ejemplares_disponibles += 1
            db.session.commit()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
