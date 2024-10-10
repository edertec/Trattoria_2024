from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

app = Flask(__name__)

# Definir uma chave secreta para gerenciar sessões
app.config['SECRET_KEY'] = 'CETEC'

# Configurações adicionais (banco de dados, autenticação, etc.)
app.config.from_object(Config)

# Inicialização das extensões
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Importar rotas e modelos após a inicialização do app
from app import routes, models

# Criar tabelas do banco de dados se ainda não existirem
with app.app_context():
    db.create_all()
