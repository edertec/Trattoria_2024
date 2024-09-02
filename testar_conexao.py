from app import app, db  # Certifique-se de que 'app' é definido em '__init__.py'
from app.models import Comprador, Ingresso

def test_database_connection():
    with app.app_context():
        try:
            # Testando a conexão e consulta básica às tabelas
            compradores = Comprador.query.first()
            ingressos = Ingresso.query.first()
        

            print("Teste de conexão com a tabela Comprador:")
            if compradores:
                print(f"Primeiro comprador: {compradores.nome}")
            else:
                print("Nenhum comprador encontrado.")

            print("Teste de conexão com a tabela Ingresso:")
            if ingressos:
                print(f"Primeiro ingresso para o evento: {ingressos.evento}")
            else:
                print("Nenhum ingresso encontrado.")

            print("Conexão com o banco de dados foi bem-sucedida.")
        except Exception as e:
            print(f"Falha ao conectar com o banco de dados: {e}")

if __name__ == '__main__':
    test_database_connection()
