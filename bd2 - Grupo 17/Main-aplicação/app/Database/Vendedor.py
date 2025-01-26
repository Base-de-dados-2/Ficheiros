from .db_manager import *
from ..utils import listToJson_

def create_vendedor(id_utilizador, cargo, vendas_realizadas):
    """Cria um novo vendedor no banco de dados."""
    try:
        print(f"ID Utilizador: {id_utilizador}, Cargo: {cargo}, Vendas Realizadas: {vendas_realizadas}")  # Log
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO vendedor_bd2 (id_utilizador, cargo, vendas_realizadas)
                VALUES (%s, %s, %s)
                """,
                [id_utilizador, cargo, vendas_realizadas],
            )
            get_pg_connection().commit()
        print("Vendedor criado com sucesso")  # Log
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao criar vendedor: {e}")


def update_vendedor(id_vendedor, id_utilizador=None, cargo=None, vendas_realizadas=None):
    """Atualiza os dados de um vendedor existente no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE vendedor_bd2
                SET id_utilizador = COALESCE(%s, id_utilizador),
                    cargo = COALESCE(%s, cargo),
                    vendas_realizadas = COALESCE(%s, vendas_realizadas)
                WHERE id_vendedor = %s
                """,
                [id_utilizador, cargo, vendas_realizadas, id_vendedor],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar vendedor: {e}")


def delete_vendedor(id_vendedor):
    """Exclui um vendedor pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM vendedor_bd2
                WHERE id_vendedor = %s
                """,
                [id_vendedor],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir vendedor: {e}")


def readone_vendedor(id_vendedor):
    """Obtém os dados de um vendedor específico pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM vendedor_bd2
                WHERE id_vendedor = %s
                """,
                [id_vendedor],
            )
            result = cursor.fetchone()
            return listToJson_([result], ['id_vendedor', 'id_utilizador', 'cargo', 'vendas_realizadas'])
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar vendedor: {e}")


def readjson_vendedor():
    """Obtém todos os vendedores no banco de dados com informações de utilizador."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute("""
                SELECT v.id_vendedor, v.cargo, v.vendas_realizadas, u.id_utilizador, u.nome
                FROM vendedor_bd2 v
                JOIN utilizador_bd2 u ON v.id_utilizador = u.id_utilizador
            """)
            result = cursor.fetchall()
            return listToJson_(result, ['id_vendedor', 'cargo', 'vendas_realizadas', 'id_utilizador', 'nome'])
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar vendedores: {e}")
