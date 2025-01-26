from .db_manager import *
from ..utils import listToJson_

columns = ['id_manutencao', 'id_veiculo', 'data_manutencao', 'tipo_manutencao', 'descricao', 'oficina_responsavel']

def create_manutencao(id_veiculo, data_manutencao, tipo_manutencao, descricao, oficina_responsavel):
    """Cria uma nova manutenção no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Manutencao_BD2 (ID_Veiculo, Data_Manutencao, Tipo_Manutencao, Descricao, Oficina_Responsavel)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [id_veiculo, data_manutencao, tipo_manutencao, descricao, oficina_responsavel],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao criar manutenção: {e}")

def update_manutencao(id_manutencao, id_veiculo=None, data_manutencao=None, tipo_manutencao=None, descricao=None, oficina_responsavel=None):
    """Atualiza os dados de uma manutenção existente."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE Manutencao_BD2
                SET ID_Veiculo = COALESCE(%s, ID_Veiculo),
                    Data_Manutencao = COALESCE(%s, Data_Manutencao),
                    Tipo_Manutencao = COALESCE(%s, Tipo_Manutencao),
                    Descricao = COALESCE(%s, Descricao),
                    Oficina_Responsavel = COALESCE(%s, Oficina_Responsavel)
                WHERE ID_Manutencao = %s
                """,
                [id_veiculo, data_manutencao, tipo_manutencao, descricao, oficina_responsavel, id_manutencao],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar manutenção: {e}")

def delete_manutencao(id_manutencao):
    """Exclui uma manutenção pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM Manutencao_BD2
                WHERE ID_Manutencao = %s
                """,
                [id_manutencao],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir manutenção: {e}")

def readone_manutencao(id_manutencao):
    """Obtém os dados de uma manutenção específica pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM Manutencao_BD2
                WHERE ID_Manutencao = %s
                """,
                [id_manutencao],
            )
            result = cursor.fetchone()
            return listToJson_([result], columns)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar manutenção: {e}")

def readjson_manutencao():
    """Obtém todas as manutenções da tabela Manutencao_BD2 em formato JSON."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM Manutencao_BD2")
            result = cursor.fetchall()
            return listToJson_(result, columns)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar manutenções: {e}")
