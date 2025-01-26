from datetime import datetime
import ast
import json
from decimal import Decimal

def listToJson(json):
    return json[0][0]

def listToJson_(data, columns):

    vehicle_dict = [dict(zip(columns, vehicle)) for vehicle in data]    
    return vehicle_dict

def getFirstElement(json):
    return json[0][0][0]

def formatar_data(data_original):
    data_obj = datetime.strptime(data_original, '%Y-%m-%dT%H:%M:%S.%f')
    return data_obj.strftime('%d-%m-%Y %H:%M:%S')

def stringToArray(string):
    partes = string.strip('()').split(',')

    # Remover espaços extras e retornar a lista resultante
    return [parte.strip() for parte in partes]

def getOnlyElement(string):
	try:
		tuple_value = ast.literal_eval(string)
		if isinstance(tuple_value, tuple) and len(tuple_value) == 1:
			extracted_value = tuple_value[0]
			if isinstance(extracted_value, int):
				return extracted_value
			else:
				print("Tuple element is not an integer.")
				return ""
		else:
			print("Invalid tuple format.")
			return ""
	except (SyntaxError, ValueError) as e:
		print(f"Error: {e}")
		return ""

def getOnlyElementString(string):
	try:
		tuple_value = ast.literal_eval(string)
		if isinstance(tuple_value, tuple) and len(tuple_value) == 1:
			extracted_value = tuple_value[0]
			if isinstance(extracted_value, str):
				return extracted_value
			else:
				print("Tuple element is not an integer.")
				return ""
		else:
			print("Invalid tuple format.")
			return ""
	except (SyntaxError, ValueError) as e:
		print(f"Error: {e}")
		return ""

def corrigir_json(lista):
    return json.dumps(lista)

def tojson(json):
	try:
		json_corrigido = corrigir_json(json)
		print(json_corrigido)
		json_completo = json.loads(json_corrigido)
		print(json_completo)
	except:
		return "Ocorreu algum erro"
