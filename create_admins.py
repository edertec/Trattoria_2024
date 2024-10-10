from app import app, db, bcrypt
from app.models import Comprador_registrado3

# Lista de e-mails e senhas para usuários administradores
admin_users = [
    {"name": "Eduardo", "email": "pedroso@gmail.com", "password": "adminpassword1", "cpf":"69", "numero":"69"},
    {"name": "Estevan", "email": "estevan@gmail.com", "password": "senha", "cpf":"24", "numero":"24"}
]

# Função para adicionar usuários administradores
def create_admin_users():
    with app.app_context():
        for user_data in admin_users:
            # Verifica se o e-mail já está no banco de dados
            if Comprador_registrado3.query.filter_by(email=user_data["email"]).first() is None:
                senha = bcrypt.generate_password_hash(user_data["password"]).decode('utf8')

                # Cria um novo usuário administrador
                user = Comprador_registrado3(name=user_data["name"], email=user_data["email"],cpf=user_data["cpf"],numero=user_data["numero"],is_admin=True,senha=senha)

                db.session.add(user)
        
        db.session.commit()

if __name__ == "__main__":
    create_admin_users()