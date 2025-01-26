from .db_manager import *  # Importa métodos de gerenciamento do banco de dados
from ..utils import listToJson_

def create_promocao(nome_promocao, id_veiculo, categoria, data_inicio, data_terminada, percentual_desconto, descricao):
    """Cria uma nova promoção no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO promocao_bd2 (nome_promocao, id_veiculo, categoria, data_inicio, data_terminada, percentual_desconto, descricao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                [nome_promocao, id_veiculo, categoria, data_inicio, data_terminada, percentual_desconto, descricao],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao criar promoção: {e}")

def update_promocao(id_promocao, nome_promocao=None, id_veiculo=None, categoria=None, data_inicio=None, data_terminada=None, percentual_desconto=None, descricao=None):
    """Atualiza os dados de uma promoção existente no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE promocao_bd2
                SET nome_promocao = COALESCE(%s, nome_promocao),
                    id_veiculo = COALESCE(%s, id_veiculo),
                    categoria = COALESCE(%s, categoria),
                    data_inicio = COALESCE(%s, data_inicio),
                    data_terminada = COALESCE(%s, data_terminada),
                    percentual_desconto = COALESCE(%s, percentual_desconto),
                    descricao = COALESCE(%s, descricao)
                WHERE id_promocao = %s
                """,
                [nome_promocao, id_veiculo, categoria, data_inicio, data_terminada, percentual_desconto, descricao, id_promocao],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar promoção: {e}")

def delete_promocao(id_promocao):
    """Exclui uma promoção pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM promocao_bd2
                WHERE id_promocao = %s
                """,
                [id_promocao],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir promoção: {e}")

def readone_promocao(id_promocao):
    """Obtém os dados de uma promoção específica pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM promocao_bd2
                WHERE id_promocao = %s
                """,
                [id_promocao],
            )
            result = cursor.fetchone()
            return listToJson_(
                [result],
                ['id_promocao', 'nome_promocao', 'id_veiculo', 'categoria', 'data_inicio', 'data_terminada', 'percentual_desconto', 'descricao']
            )
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar promoção: {e}")

def readjson_promocao():
    """Obtém todas as promoções no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM promocao_bd2")
            result = cursor.fetchall()
            return listToJson_(
                result,
                ['id_promocao', 'nome_promocao', 'id_veiculo', 'categoria', 'data_inicio', 'data_terminada', 'percentual_desconto', 'descricao']
            )
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar promoções: {e}")
