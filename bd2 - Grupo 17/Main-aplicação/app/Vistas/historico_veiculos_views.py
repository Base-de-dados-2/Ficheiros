from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..Database.historicoveiculos import (
    create_historico,
    update_historico,
    delete_historico,
    readone_historico,
    readjson_historico
)
from ..Formularios.historicoveiculos_form import FormHistoricoVeiculo
from ..Database.Veiculos import readjson_veiculo

# Listar todos os históricos de veículos
def historicoveiculo_listar(request):
    try:
        historicos = readjson_historico()
        return render(request, 'Historico_veiculo/listar.html', {'historicos': historicos})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Exibir detalhes de um histórico de veículo
def historicoveiculo_detalhes(request, id_historico):
    try:
        # Busca o histórico específico pelo ID
        historico = readone_historico(id_historico)
        if historico:
            historico["id_veiculo"] = int(historico["id_veiculo"])  # Garante que seja um número inteiro
        
        # Obtém todos os veículos
        veiculos = readjson_veiculo()  # Função que retorna todos os veículos

        return render(request, 'Historico_veiculo/detalhes.html', {'historico': historico, 'veiculos': veiculos})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")



# Registrar um novo histórico de veículo
def historicoveiculo_registar(request):
    try:
        # Busca todos os veículos cadastrados para o formulário
        veiculos = readjson_veiculo()  # A função `readjson_veiculo` deve retornar todos os veículos cadastrados
        
        if request.method == 'POST':
            form = FormHistoricoVeiculo(request.POST)
            if form.is_valid():
                # Recupera os dados do formulário e cria o histórico
                create_historico(
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    manutencoes=form.cleaned_data['manutencoes'],
                    acidentes=form.cleaned_data['acidentes'],
                    dono_anterior=form.cleaned_data['dono_anterior']
                )
                return redirect('historico_listar')  # Redireciona para a lista de históricos
            else:
                return HttpResponse(f"Formulário inválido: {form.errors}")
        
        else:
            # Se for GET, exibe o formulário
            form = FormHistoricoVeiculo()

        return render(request, 'Historico_veiculo/registar.html', {
            'form': form,
            'veiculos': veiculos
        })
    
    except Exception as e:
        return HttpResponse(f"Erro ao registrar o histórico do veículo: {e}")

# Atualizar um histórico de veículo existente
def historicoveiculo_atualizar(request, id_historico):
    try:
        # Obter o histórico específico
        historico = readone_historico(id_historico)

        # Verifica se o histórico existe
        if not historico:
            return HttpResponse("Histórico não encontrado.", status=404)

        # Obter todos os veículos disponíveis
        veiculos = readjson_veiculo()  # Função que retorna todos os veículos cadastrados

        if request.method == 'POST':
            form = FormHistoricoVeiculo(request.POST)
            if form.is_valid():
                update_historico(
                    id_historico=id_historico,
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    manutencoes=form.cleaned_data['manutencoes'],
                    acidentes=form.cleaned_data['acidentes'],
                    dono_anterior=form.cleaned_data['dono_anterior']
                )
                return redirect('historico_listar')
        else:
            # Inicializando o formulário com os dados do histórico
            form = FormHistoricoVeiculo(initial={
                'id_veiculo': historico['id_veiculo'],  # Acesso ao valor do dicionário com a chave
                'manutencoes': historico['manutencoes'],
                'acidentes': historico['acidentes'],
                'dono_anterior': historico['dono_anterior'],
            })

        return render(request, 'Historico_veiculo/editar.html', {
            'form': form,
            'veiculos': veiculos,  # Lista de veículos
        })

    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}", status=500)




# Remover um histórico de veículo
def historicoveiculo_remover(request, id_historico):
    try:
        delete_historico(id_historico)
        return redirect('historico_listar')
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao remover o histórico de veículo: {e}")
