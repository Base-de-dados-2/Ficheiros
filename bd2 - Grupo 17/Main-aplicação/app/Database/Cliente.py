from .db_manager import *
from ..utils import listToJson_

def create_cliente(id_utilizador, historico_compras, interesse_veiculos):
    """Cria um novo cliente no banco de dados."""
    try:
        print(f"ID Utilizador: {id_utilizador}, Histórico de Compras: {historico_compras}, Interesse de Veículos: {interesse_veiculos}")  # Log
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO cliente_bd2 (id_utilizador, historico_compras, interesse_veiculos)
                VALUES (%s, %s, %s)
                """,
                [id_utilizador, historico_compras, interesse_veiculos],
            )
            get_pg_connection().commit()
        print("Cliente criado com sucesso")  # Log
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao criar cliente: {e}")


def update_cliente(id_cliente, id_utilizador=None, historico_compras=None, interesse_veiculos=None):
    """Atualiza os dados de um cliente existente no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE cliente_bd2
                SET id_utilizador = COALESCE(%s, id_utilizador),
                    historico_compras = COALESCE(%s, historico_compras),
                    interesse_veiculos = COALESCE(%s, interesse_veiculos)
                WHERE id_cliente = %s
                """,
                [id_utilizador, historico_compras, interesse_veiculos, id_cliente],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar cliente: {e}")

def remover_cliente(id_cliente):
    """Exclui um cliente pelo ID após verificar associações com outras tabelas."""
    try:
        with get_pg_cursor() as cursor:
            # Verifica se o cliente está associado a test-drives
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM testdrive_bd2 
                WHERE id_cliente = %s
                """,
                [id_cliente],
            )
            result_testdrive = cursor.fetchone()

            if result_testdrive[0] > 0:  # Cliente associado a test-drives
                raise RuntimeError("Não é possível remover o cliente porque ele está associado a um test-drive.")

            # Verifica se o cliente está associado a transações de venda
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM transacaovenda_bd2 
                WHERE id_cliente = %s
                """,
                [id_cliente],
            )
            result_transacaovenda = cursor.fetchone()

            # Se não houver associações, remove o cliente
            cursor.execute(
                """
                DELETE FROM cliente_bd2
                WHERE id_cliente = %s
                """,
                [id_cliente],
            )
            get_pg_connection().commit()

    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir cliente: {e}")


def readone_cliente(id_cliente):
    """Obtém os dados de um cliente específico pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM cliente_bd2
                WHERE id_cliente = %s
                """,
                [id_cliente],
            )
            result = cursor.fetchone()
            return listToJson_([result], ['id_cliente', 'id_utilizador', 'historico_compras', 'interesse_veiculos'])
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar cliente: {e}")

def readjson_cliente():
    """Obtém todos os clientes com os nomes dos utilizadores do banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            # Realiza o JOIN para incluir o nome do utilizador e o campo interesse_veiculos
            cursor.execute("""
                SELECT 
                    cliente.id_cliente, 
                    cliente.id_utilizador, 
                    cliente.historico_compras, 
                    cliente.interesse_veiculos,
                    utilizador.nome
                FROM cliente_bd2 AS cliente
                JOIN utilizador_bd2 AS utilizador
                ON cliente.id_utilizador = utilizador.id_utilizador
            """)
            result = cursor.fetchall()

            # Retorna o resultado com os campos convertidos
            return listToJson_(
                result, 
                ['id_cliente', 'id_utilizador', 'historico_compras', 'interesse_veiculos', 'nome']
            )
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar clientes: {e}")




