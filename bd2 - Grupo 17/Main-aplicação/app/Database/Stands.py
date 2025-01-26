from .db_manager import *
from ..utils import listToJson_

# Definindo as colunas da tabela Stand
columns = ['id_stand', 'nome', 'localizacao', 'responsavel']

# Função para criar um novo stand no banco de dados
def create_stand(nome, localizacao, responsavel):
    """Cria um novo stand na tabela Stand_BD2."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Stand_BD2 
                (Nome, Localizacao, Responsavel)
                VALUES (%s, %s, %s)
                """,
                [nome, localizacao, responsavel],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao criar stand: {e}")

# Função para atualizar um stand existente no banco de dados
def update_stand(id_stand, nome=None, localizacao=None, responsavel=None):
    """Atualiza os dados de um stand existente na tabela Stand_BD2."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE Stand_BD2
                SET Nome = COALESCE(%s, Nome),
                    Localizacao = COALESCE(%s, Localizacao),
                    Responsavel = COALESCE(%s, Responsavel)
                WHERE ID_Stand = %s
                """,
                [nome, localizacao, responsavel, id_stand],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar stand: {e}")

# Função para excluir um stand do banco de dados
def delete_stand(id_stand):
    """Exclui um stand da tabela Stand_BD2 pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM Stand_BD2
                WHERE ID_Stand = %s
                """,
                [id_stand],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir stand: {e}")

# Função para buscar um único stand no banco de dados, baseado no ID
def readone_stand(id_stand):
    """Obtém os dados de um stand específico pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM Stand_BD2
                WHERE ID_Stand = %s
                """,
                [id_stand],
            )
            result = cursor.fetchone()
            return listToJson_([result], columns)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar stand: {e}")

# Função para buscar todos os stands no banco de dados
def readjson_stand():
    """Obtém todos os stands da tabela Stand_BD2 em formato JSON."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM Stand_BD2")
            result = cursor.fetchall()  # Isso retorna uma lista de tuplas
            # Convertendo a lista de tuplas para uma lista de dicionários
            return [{"id_stand": row[0], "nome": row[1], "localizacao": row[2], "responsavel": row[3]} for row in result]
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar stands: {e}")
