from app import db

class Comprador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

from app import db

class Ingresso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evento = db.Column(db.String(150), nullable=False)
    comprador_id = db.Column(db.Integer, db.ForeignKey('comprador.id'))
    comprador = db.relationship('Comprador', backref=db.backref('ingressos', lazy=True))
    titular = db.Column(db.String(100), nullable=False)
    email_contato = db.Column(db.String(100), nullable=False)
    pago = db.Column(db.Boolean, default=False, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    restricoes_alimentares = db.Column(db.String(255))

    def __repr__(self):
        return f'<Ingresso {self.evento} para {self.titular}>'

