from .db_manager import *  
from ..utils import listToJson, listToJson_
columns = ['id', 'marca', 'modelo', 'ano', 'preco', 'quilometragem', 'cor', 'combustivel', 'id_stand', 'id_fornecedor']

# Função para criar um veículo no banco de dados
def create_veiculo(marca, modelo, ano, preco, quilometragem, cor, tipo_combustivel, id_stand, id_fornecedor):
    """Cria um novo veículo na tabela Veiculo_BD2."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Veiculo_BD2 
                (Marca, Modelo, Ano, Preco, Quilometragem, Cor, Tipo_Combustivel, ID_Stand, ID_Fornecedor)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [marca, modelo, ano, preco, quilometragem, cor, tipo_combustivel, id_stand, id_fornecedor],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao criar veículo: {e}")

# Função para atualizar um veículo existente no banco de dados
def update_veiculo(id_veiculo, marca=None, modelo=None, ano=None, preco=None, quilometragem=None, cor=None, tipo_combustivel=None, id_stand=None, id_fornecedor=None):
    """Atualiza os dados de um veículo existente na tabela Veiculo_BD2."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE Veiculo_BD2
                SET Marca = COALESCE(%s, Marca),
                    Modelo = COALESCE(%s, Modelo),
                    Ano = COALESCE(%s, Ano),
                    Preco = COALESCE(%s, Preco),
                    Quilometragem = COALESCE(%s, Quilometragem),
                    Cor = COALESCE(%s, Cor),
                    Tipo_Combustivel = COALESCE(%s, Tipo_Combustivel),
                    ID_Stand = COALESCE(%s, ID_Stand),
                    ID_Fornecedor = COALESCE(%s, ID_Fornecedor)
                WHERE ID_Veiculo = %s
                """,
                [marca, modelo, ano, preco, quilometragem, cor, tipo_combustivel, id_stand, id_fornecedor, id_veiculo],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar veículo: {e}")


# Função para excluir um veículo do banco de dados
def delete_veiculo(id_veiculo):
    """Exclui um veículo da tabela Veiculo_BD2 pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM Veiculo_BD2
                WHERE ID_Veiculo = %s
                """,
                [id_veiculo],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir veículo: {e}")

# Função para buscar um único veículo no banco de dados, baseado no ID
def readone_veiculo(id_veiculo):
    """Obtém os dados de um veículo específico pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM Veiculo_BD2
                WHERE ID_Veiculo = %s
                """,
                [id_veiculo],
            )
            result = cursor.fetchone()
            return listToJson_([result], columns)  # Corrigido
        veiculo = readone_veiculo(id)
        print(veiculo)  # Para ver como os dados estão sendo retornados

    except Exception as e:
        raise RuntimeError(f"Erro ao buscar veículo: {e}")


# Função para buscar todos os veículos no banco de dados
def readjson_veiculo():
    """Obtém todos os veículos da tabela Veiculo_BD2 em formato JSON."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM Veiculo_BD2")
            result = cursor.fetchall()
            result =  listToJson_(result, columns)
            print('result', result)
            return result
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar veículos: {e}")

# Função para buscar veículos usados no banco de dados
def readjson_veiculo_usados():
    """Obtém veículos usados (com quilometragem maior que zero) em formato JSON."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM Veiculo_BD2
                WHERE Quilometragem > 0
                """
            )
            result = cursor.fetchall()
            return listToJson(result)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar veículos usados: {e}")
    

def remover_veiculo(id_veiculo):
    """Exclui um veículo pelo ID após verificar associações com outras tabelas."""
    try:
        with get_pg_cursor() as cursor:
            # Verifica se o id_veiculo está associado a uma promoção
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM promocao_bd2 
                WHERE id_veiculo = %s
                """,
                [id_veiculo],
            )
            result_promocao = cursor.fetchone()

            if result_promocao[0] > 0:  # Se o veículo está associado a uma promoção
                raise RuntimeError("Não é possível remover o veículo porque ele está associado a uma promoção.")

            # Verifica se o id_veiculo está associado a um test-drive
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM testdrive_bd2 
                WHERE id_veiculo = %s
                """,
                [id_veiculo],
            )
            result_testdrive = cursor.fetchone()

            if result_testdrive[0] > 0:  # Se o veículo está associado a um test-drive
                raise RuntimeError("Não é possível remover o veículo porque ele está associado a um test-drive.")

            # Verifica se o id_veiculo está associado a uma transação de venda
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM transacaovenda_bd2 
                WHERE id_veiculo = %s
                """,
                [id_veiculo],
            )
            result_transacaovenda = cursor.fetchone()

            if result_transacaovenda[0] > 0:  # Se o veículo está associado a uma transação de venda
                raise RuntimeError("Não é possível remover o veículo porque ele está associado a uma transação de venda.")

            # Verifica se o id_veiculo está associado a uma manutenção
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM manutencao_bd2 
                WHERE id_veiculo = %s
                """,
                [id_veiculo],
            )
            result_manutencao = cursor.fetchone()

            if result_manutencao[0] > 0:  # Se o veículo está associado a uma manutenção
                raise RuntimeError("Não é possível remover o veículo porque ele está associado a uma manutenção.")

            # Se não houver associações, remove o veículo
            cursor.execute(
                """
                DELETE FROM veiculo_bd2
                WHERE id_veiculo = %s
                """,
                [id_veiculo],
            )
            get_pg_connection().commit()

    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir veículo: {e}")

