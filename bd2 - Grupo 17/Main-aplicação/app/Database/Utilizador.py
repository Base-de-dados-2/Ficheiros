from .db_manager import *
from ..utils import  listToJson_

# Função para criar um novo utilizador
def create_utilizador(nome, email, telefone, tipo_utilizador, data_criacao):
    """Cria um novo utilizador no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO utilizador_bd2 (nome, email, telefone, tipo_utilizador, data_criacao)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [nome, email, telefone, tipo_utilizador, data_criacao],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao criar utilizador: {e}")

# Função para atualizar um utilizador existente
def update_utilizador(id_utilizador, nome, email, telefone, tipo_utilizador, data_criacao):
    """Atualiza os dados de um utilizador existente."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE utilizador_bd2
                SET nome = %s, email = %s, telefone = %s, tipo_utilizador = %s, data_criacao = %s
                WHERE id_utilizador = %s
                """,
                [nome, email, telefone, tipo_utilizador, data_criacao, id_utilizador],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar utilizador: {e}")

# Função para excluir um utilizador
def delete_utilizador(id_utilizador):
    """Exclui um utilizador pelo ID após verificar associações com clientes e vendedores."""
    try:
        with get_pg_cursor() as cursor:
            # Verifica se o id_utilizador está associado a um cliente
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM cliente_bd2 
                WHERE id_utilizador = %s
                """,
                [id_utilizador],
            )
            result_cliente = cursor.fetchone()

            if result_cliente[0] > 0:  # Se há associações com clientes, lança um erro
                raise RuntimeError("Não é possível remover o utilizador porque ele está associado a um cliente.")

            # Verifica se o id_utilizador está associado a um vendedor
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM vendedor_bd2 
                WHERE id_utilizador = %s
                """,
                [id_utilizador],
            )
            result_vendedor = cursor.fetchone()

            if result_vendedor[0] > 0:  # Se há associações com vendedores, lança um erro
                raise RuntimeError("Não é possível remover o utilizador porque ele está associado a um vendedor.")

            # Se não houver associações, remove o utilizador
            cursor.execute(
                """
                DELETE FROM utilizador_bd2
                WHERE id_utilizador = %s
                """,
                [id_utilizador],
            )
            get_pg_connection().commit()

    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir utilizador: {e}")






# Função para buscar um único utilizador pelo ID
def readone_utilizador(id_utilizador):
    """Obtém os dados de um utilizador específico pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM utilizador_bd2
                WHERE id_utilizador = %s
                """,
                [id_utilizador],
            )
            result = cursor.fetchone()

            # Verificar se o resultado é None
            if result is None:
                raise RuntimeError(f"Utilizador com ID {id_utilizador} não encontrado.")

            # Print para depuração
            print("Dados do utilizador:", result)  # Adicionando o print

            # Convertendo o resultado para um formato que pode ser acessado no template
            return dict(zip([column[0] for column in cursor.description], result))

    except Exception as e:
        raise RuntimeError(f"Erro ao buscar utilizador: {e}")




# Função para buscar todos os utilizadores
def readjson_utilizador():
    """Obtém todos os utilizadores no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            # Alterando a consulta para incluir todos os campos necessários
            cursor.execute("SELECT id_utilizador, nome, email, telefone, tipo_utilizador, data_criacao FROM utilizador_bd2")  
            result = cursor.fetchall()

            # Agora todos os campos estão presentes
            return listToJson_(result, ['id_utilizador', 'nome', 'email', 'telefone', 'tipo_utilizador', 'data_criacao'])
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar utilizadores: {e}")

