from .db_manager import *
from ..utils import listToJson_

columns = ['id_fornecedor', 'nome', 'contato', 'veiculos_fornecedor']

def create_fornecedor(nome, contato, veiculos_fornecedor):
    """Cria um novo fornecedor no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Fornecedor_BD2 (Nome, Contato, Veiculos_Fornecedor)
                VALUES (%s, %s, %s)
                """,
                [nome, contato, veiculos_fornecedor],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao criar fornecedor: {e}")

def update_fornecedor(id_fornecedor, nome=None, contato=None, veiculos_fornecedor=None):
    """Atualiza os dados de um fornecedor existente."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE Fornecedor_BD2
                SET Nome = COALESCE(%s, Nome),
                    Contato = COALESCE(%s, Contato),
                    Veiculos_Fornecedor = COALESCE(%s, Veiculos_Fornecedor)
                WHERE ID_Fornecedor = %s
                """,
                [nome, contato, veiculos_fornecedor, id_fornecedor],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar fornecedor: {e}")

def delete_fornecedor(id_fornecedor):
    """Exclui um fornecedor pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM Fornecedor_BD2
                WHERE ID_Fornecedor = %s
                """,
                [id_fornecedor],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir fornecedor: {e}")

def readone_fornecedor(id_fornecedor):
    """Obtém os dados de um fornecedor específico pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM Fornecedor_BD2
                WHERE ID_Fornecedor = %s
                """,
                [id_fornecedor],
            )
            result = cursor.fetchone()
            return listToJson_([result], columns)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar fornecedor: {e}")

def readjson_fornecedor():
    """Obtém todos os fornecedores da tabela Fornecedor_BD2 em formato JSON."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM Fornecedor_BD2")
            result = cursor.fetchall()
            return listToJson_(result, columns)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar fornecedores: {e}")
