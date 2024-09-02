from app import app, db
from app.models import Comprador, Ingresso

def add_data():
    try:
        with app.app_context():
            # Criando novos objetos
            comprador1 = Comprador(nome="João Silva", email="joao.silva@example.com")
            comprador2 = Comprador(nome="Maria Oliveira", email="maria.oliveira@example.com")

            # Adicionando objetos à sessão do banco de dados
            db.session.add(comprador1)
            db.session.add(comprador2)

            # Salvando as mudanças no banco de dados
            db.session.commit()

            # Criando ingressos associados ao primeiro comprador
            ingresso1 = Ingresso(evento="Concerto de Rock", comprador_id=comprador1.id)
            ingresso2 = Ingresso(evento="Festival de Jazz", comprador_id=comprador1.id)

            # Adicionando e salvando os ingressos
            db.session.add(ingresso1)
            db.session.add(ingresso2)
            db.session.commit()

            print("Dados adicionados com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar dados: {e}")

def fetch_data():
    try:
        with app.app_context():
            # Consultando todos os compradores
            compradores = Comprador.query.all()
            print("Compradores:")
            for comprador in compradores:
                print(f"{comprador.id} - {comprador.nome} - {comprador.email}")

            # Consultando todos os ingressos
            ingressos = Ingresso.query.all()
            print("\nIngressos:")
            for ingresso in ingressos:
                print(f"{ingresso.id} - {ingresso.evento} - Comprador: {ingresso.comprador.nome}")

            print("Consulta completada com sucesso.")
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")

if __name__ == '__main__':
    # Verificando se a tabela está vazia e então adicionando dados
    if not Comprador.query.first():
        add_data()

    # Buscando dados adicionados
    fetch_data()
