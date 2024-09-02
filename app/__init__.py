from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')  # Certifique-se de que config.Config está corretamente configurado

db = SQLAlchemy(app)

# Importando modelos
from app import models  # Assegure-se de que todos os seus modelos estão definidos em app/models.py

# Recriando as tabelas a cada inicialização para teste
with app.app_context():
    # db.drop_all()  # Remove todas as tabelas
    db.create_all()  # Cria todas as tabelas baseadas nos modelos

# Importando rotas após a criação das tabelas
from app import routes  # Assegure-se de que suas rotas estão definidas em app/routes.py
