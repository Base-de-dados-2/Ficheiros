from .db_manager import *
from ..utils import listToJson_

# Definindo as colunas da tabela TransacaoVenda_BD2
columns = ['id_transacao', 'id_cliente', 'id_veiculo', 'id_vendedor', 'data_venda', 'valor_venda']

# Função para criar uma nova transação de venda no banco de dados
def create_transacaovenda(id_cliente, id_veiculo, id_vendedor, data_venda, valor_venda):
    """Cria uma transação de venda no banco de dados com tratamento de erro."""
    try:
        with get_pg_cursor() as cursor:
            # Verifica se os dados de cliente, veículo e vendedor são válidos antes de inserir
            cursor.execute("SELECT 1 FROM cliente_bd2 WHERE id_cliente = %s", [id_cliente])
            if cursor.fetchone() is None:
                raise ValueError(f"Cliente com id {id_cliente} não encontrado.")
            
            cursor.execute("SELECT 1 FROM veiculo_bd2 WHERE id_veiculo = %s", [id_veiculo])
            if cursor.fetchone() is None:
                raise ValueError(f"Veículo com id {id_veiculo} não encontrado.")
            
            cursor.execute("SELECT 1 FROM vendedor_bd2 WHERE id_vendedor = %s", [id_vendedor])
            if cursor.fetchone() is None:
                raise ValueError(f"Vendedor com id {id_vendedor} não encontrado.")
            
            # Inserção de dados após validação
            cursor.execute("""
                INSERT INTO transacaovenda_bd2 (id_cliente, id_veiculo, id_vendedor, data_venda, valor_venda)
                VALUES (%s, %s, %s, %s, %s)
            """, [id_cliente, id_veiculo, id_vendedor, data_venda, valor_venda])

            # Confirma a transação após a execução bem-sucedida
            get_pg_connection().commit()
            
    except Exception as e:
        # Se ocorreu algum erro, reverte a transação
        get_pg_connection().rollback()
        print(f"Erro ao tentar registrar transação de venda: {str(e)}")
        raise RuntimeError(f"Erro ao registrar transação de venda: {e}")


# Função para atualizar uma transação de venda existente no banco de dados
def update_transacaovenda(id_transacao, id_cliente=None, id_veiculo=None, id_vendedor=None, data_venda=None, valor_venda=None):
    """Atualiza os dados de uma transação de venda existente na tabela TransacaoVenda_BD2."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                UPDATE TransacaoVenda_BD2
                SET ID_Cliente = COALESCE(%s, ID_Cliente),
                    ID_Veiculo = COALESCE(%s, ID_Veiculo),
                    ID_Vendedor = COALESCE(%s, ID_Vendedor),
                    Data_Venda = COALESCE(%s, Data_Venda),
                    Valor_Venda = COALESCE(%s, Valor_Venda)
                WHERE ID_Transacao = %s
                """,
                [id_cliente, id_veiculo, id_vendedor, data_venda, valor_venda, id_transacao],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao atualizar transação de venda: {e}")

# Função para excluir uma transação de venda do banco de dados
def delete_transacaovenda(id_transacao):
    """Exclui uma transação de venda da tabela TransacaoVenda_BD2 pelo ID."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM TransacaoVenda_BD2
                WHERE ID_Transacao = %s
                """,
                [id_transacao],
            )
            get_pg_connection().commit()
    except Exception as e:
        get_pg_connection().rollback()
        raise RuntimeError(f"Erro ao excluir transação de venda: {e}")

# Função para buscar uma única transação de venda no banco de dados, baseado no ID
def readone_transacaovenda(id_transacao):
    """Obtém os detalhes de uma transação de venda específica."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute(
                """
                SELECT id_transacao, id_cliente, id_veiculo, id_vendedor, data_venda, valor_venda
                FROM transacaovenda_bd2
                WHERE id_transacao = %s
                """,
                [id_transacao],
            )
            result = cursor.fetchone()
            return {
                'id_transacao': result[0],
                'id_cliente': result[1],
                'id_veiculo': result[2],
                'id_vendedor': result[3],
                'data_venda': result[4],
                'valor_venda': result[5],
            } if result else None
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar transação: {e}")


# Função para buscar todas as transações de venda no banco de dados
def readjson_transacaovenda():
    """Obtém todas as transações de venda da tabela TransacaoVenda_BD2 em formato JSON."""
    try:
        with get_pg_cursor() as cursor:
            cursor.execute("SELECT * FROM TransacaoVenda_BD2")
            result = cursor.fetchall()  # Isso retorna uma lista de tuplas
            # Convertendo a lista de tuplas para uma lista de dicionários
            return [
                {
                    "id_transacao": row[0],
                    "id_cliente": row[1],
                    "id_veiculo": row[2],
                    "id_vendedor": row[3],
                    "data_venda": row[4],
                    "valor_venda": row[5],
                }
                for row in result
            ]
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar transações de venda: {e}")
