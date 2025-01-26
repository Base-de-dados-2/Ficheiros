from .db_manager import *
from ..utils import listToJson_

# Definindo as colunas da coleção Historicoveiculos
columns = ['id_historico', 'id_veiculo', 'manutencoes', 'acidentes', 'dono_anterior']

# Função para criar um novo histórico de veículo no MongoDB
from bson import ObjectId

from bson import ObjectId

def create_historico(id_veiculo, manutencoes, acidentes, dono_anterior):
    """Cria um novo histórico de veículo no MongoDB."""
    try:
        collection = get_mg_collection('historicoveiculos_bd2')
        historico = {
            '_id': ObjectId(),  # MongoDB gera o ID automaticamente
            'id_veiculo': id_veiculo,
            'manutencoes': manutencoes,
            'acidentes': acidentes,
            'dono_anterior': dono_anterior
        }
        collection.insert_one(historico)
    except Exception as e:
        raise RuntimeError(f"Erro ao criar histórico de veículo: {e}")




# Função para atualizar um histórico de veículo existente no MongoDB
def update_historico(id_historico, id_veiculo=None, manutencoes=None, acidentes=None, dono_anterior=None):
    """Atualiza os dados de um histórico de veículo existente na coleção historicoveiculos_bd2."""
    try:
        collection = get_mg_collection('historicoveiculos_bd2')
        update_fields = {}
        
        if id_veiculo:
            update_fields['id_veiculo'] = id_veiculo
        if manutencoes:
            update_fields['manutencoes'] = manutencoes
        if acidentes:
            update_fields['acidentes'] = acidentes
        if dono_anterior:
            update_fields['dono_anterior'] = dono_anterior
        
        # Atualizando o documento com o _id convertido para ObjectId
        collection.update_one(
            {"_id": ObjectId(id_historico)},  # Filtra pelo _id (e não id_historico)
            {"$set": update_fields}          # Atualiza os campos
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar histórico de veículo: {e}")


# Função para excluir um histórico de veículo do MongoDB
def delete_historico(id_historico):
    """Exclui um histórico de veículo da coleção historicoveiculos_bd2 pelo ID."""
    try:
        collection = get_mg_collection('historicoveiculos_bd2')
        
        # Convertendo id_historico para ObjectId antes de excluir
        collection.delete_one({"_id": ObjectId(id_historico)})
    except Exception as e:
        raise RuntimeError(f"Erro ao excluir histórico de veículo: {e}")


# Função para buscar um único histórico de veículo no MongoDB, baseado no ID
from bson import ObjectId

def readone_historico(id_historico):
    """Obtém os dados de um histórico específico pelo ID."""
    try:
        collection = get_mg_collection('historicoveiculos_bd2')
        result = collection.find_one({"_id": ObjectId(id_historico)})

        if result:
            result["id_historico"] = str(result["_id"])  # Converte o _id para string
            return result
        return None
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar histórico de veículo: {e}")





# Função para buscar todos os históricos de veículos no MongoDB
def readjson_historico():
    """Obtém todos os históricos de veículos da coleção historicoveiculos_bd2 em formato JSON."""
    try:
        collection = get_mg_collection('historicoveiculos_bd2')
        result = collection.find()

        # Converte o campo `_id` para `id_historico`
        return [
            {
                "id_historico": str(row["_id"]),  # Conversão correta
                "id_veiculo": row.get("id_veiculo"),
                "manutencoes": row.get("manutencoes"),
                "acidentes": row.get("acidentes"),
                "dono_anterior": row.get("dono_anterior")
            }
            for row in result
        ]
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar históricos de veículos: {e}")

