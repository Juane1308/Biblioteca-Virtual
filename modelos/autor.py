from modelos import db

# Tabla intermedia N:M Libro ↔ Autor
libro_autor = db.Table(
    'libro_autor',
    db.Column('libro_id', db.Integer, db.ForeignKey('libro.id'), primary_key=True),
    db.Column('autor_id', db.Integer, db.ForeignKey('autor.id'), primary_key=True)
)


class Autor(db.Model):
    #Autor bibliográfico del catálogo.
    __tablename__ = 'autor'

    id           = db.Column(db.Integer, primary_key=True)
    nombre       = db.Column(db.String(150), nullable=False)
    nacionalidad = db.Column(db.String(100), nullable=True)
    fecha_nac    = db.Column(db.Date, nullable=True)

    libros = db.relationship('Libro', secondary=libro_autor, back_populates='autores')

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
