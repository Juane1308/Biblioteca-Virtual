from modelos import db
from datetime import date, timedelta


class Prestamo(db.Model):
    """Ciclo de vida de un préstamo bibliográfico."""
    __tablename__ = 'prestamo'

    id                = db.Column(db.Integer, primary_key=True)
    usuario_id        = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    libro_id          = db.Column(db.Integer, db.ForeignKey('libro.id'),   nullable=False)
    fecha_prestamo    = db.Column(db.Date, default=date.today, nullable=False)
    fecha_limite      = db.Column(db.Date, nullable=False)
    fecha_devolucion  = db.Column(db.Date, nullable=True)
    estado            = db.Column(db.String(20), default='Activo', nullable=False)

    usuario = db.relationship('Usuario', back_populates='prestamos')
    libro   = db.relationship('Libro',   back_populates='prestamos')

    def esta_vencido(self):
        return self.estado == 'Activo' and date.today() > self.fecha_limite

    def dias_restantes(self):
        return (self.fecha_limite - date.today()).days

    def registrar_devolucion(self):
        self.fecha_devolucion = date.today()
        self.estado = 'Devuelto'
        self.libro.aumentar_disponibilidad()
        db.session.commit()

