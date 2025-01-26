from .db_manager import *  # Função para conexão com o banco de dados (definida previamente)
from ..utils import listToJson_

def create_testdrive(id_cliente, id_veiculo, data_hora_testdrive, feedback_cliente):
    """Cria um novo test drive no banco de dados."""
    try:
        print(f"ID Cliente: {id_cliente}, ID Veículo: {id_veiculo}, Data e Hora: {data_hora_testdrive}, Feedback: {feedback_cliente}")  # Log
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO testdrive_bd2 (id_cliente, id_veiculo, data_hora_testdrive, feedback_cliente)
                VALUES (%s, %s, %s, %s)
                """,
                [id_cliente, id_veiculo, data_hora_testdrive, feedback_cliente],
            )
            get_pg_connection().commit()
        print("Test drive registrado com sucesso.")  # Log
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao registrar test drive: {e}")

def update_testdrive(id_testdrive, id_cliente=None, id_veiculo=None, data_hora_testdrive=None, feedback_cliente=None):
    """Atualiza os dados de um test drive existente no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE testdrive_bd2
                SET id_cliente = COALESCE(%s, id_cliente),
                    id_veiculo = COALESCE(%s, id_veiculo),
                    data_hora_testdrive = COALESCE(%s, data_hora_testdrive),
                    feedback_cliente = COALESCE(%s, feedback_cliente)
                WHERE id_testdrive = %s
                """,
                [id_cliente, id_veiculo, data_hora_testdrive, feedback_cliente, id_testdrive],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar test drive: {e}")

def delete_testdrive(id_testdrive):
    """Exclui um test drive pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM testdrive_bd2
                WHERE id_testdrive = %s
                """,
                [id_testdrive],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir test drive: {e}")

def readone_testdrive(id_testdrive):
    """Obtém os dados de um test drive específico pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM testdrive_bd2
                WHERE id_testdrive = %s
                """,
                [id_testdrive],
            )
            result = cursor.fetchone()
            return listToJson_([result], ['id_testdrive', 'id_cliente', 'id_veiculo', 'data_hora_testdrive', 'feedback_cliente'])
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar test drive: {e}")

def readjson_testdrive():
    """Obtém todos os test drives no banco de dados."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM testdrive_bd2")
            result = cursor.fetchall()
            return listToJson_(result, ['id_testdrive', 'id_cliente', 'id_veiculo', 'data_hora_testdrive', 'feedback_cliente'])
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar test drives: {e}")
