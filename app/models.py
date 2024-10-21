from app import db
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required, current_user

class Comprador_registrado3(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(500), nullable=False) 
    cpf = db.Column(db.String(20), unique=True, nullable=False)
    numero =  db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Campo que define se o usuário é um administrador

class Ingresso_registrado6(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    comprador_id = db.Column(db.Integer, db.ForeignKey('comprador_registrado3.id'))
    comprador = db.relationship('Comprador_registrado3', backref=db.backref('ingressos', lazy=True))
    titular = db.Column(db.String(100), nullable=False)
    email_contato = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    restricoes_alimentares = db.Column(db.String(255))
    pago = db.Column(db.Boolean, default=False, nullable=False)
    tipo = db.Column(db.Boolean, default=False, nullable=False)

 
    def __repr__(self):
        return f'<Ingresso {self.evento} para {self.titular}>'
    
    @classmethod
    def valor_total(cls, comprador_id):
        ingressos = cls.query.filter_by(comprador_id=comprador_id, pago=False).all()
        
        valor_crianca = 60
        valor_adulto = 120
        total = 0
        
        for ingresso in ingressos:
            if ingresso.tipo:
                total += valor_crianca
            else:
                total += valor_adulto
        
        return total




