import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..Database.Cliente import (
    create_cliente, remover_cliente, update_cliente, readone_cliente, readjson_cliente
)
from ..Database.Utilizador import readjson_utilizador  # Para buscar os IDs de Utilizador
from ..Database.Veiculos import readjson_veiculo
from ..Formularios.cliente_form import FormCliente

# Listar todos os clientes
def cliente_listar(request):
    try:
        clientes = readjson_cliente()
        veiculos = readjson_veiculo()
        
        for cliente in clientes:
            cliente['veiculos_interesse'] = []

            # Verificar e tratar o campo interesse_veiculos
            interesse_raw = cliente.get('interesse_veiculos')
            if isinstance(interesse_raw, str):  # Caso seja uma string JSON
                interesse_ids = json.loads(interesse_raw)
            elif isinstance(interesse_raw, list):  # Caso já seja uma lista
                interesse_ids = interesse_raw
            elif isinstance(interesse_raw, int):  # Caso seja um único ID
                interesse_ids = [interesse_raw]
            else:
                interesse_ids = []  # Valor inválido ou vazio
            
            # Relacionar veículos de interesse
            for veiculo in veiculos:
                if veiculo['id'] in interesse_ids:
                    cliente['veiculos_interesse'].append(veiculo)

        return render(request, 'Clientes/listar.html', {
            'clientes': clientes,
            'veiculos': veiculos,
        })

    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")







# Listar um cliente por ID
def cliente_listar_id(request, id):
    try:
        cliente = readone_cliente(id)
        utilizadores = readjson_utilizador()
        veiculos = readjson_veiculo()

        if cliente:
            cliente = cliente[0]  # Acessa o primeiro item da lista
        return render(request, 'Clientes/detalhes.html', {
            'cliente': cliente,
            'utilizadores': utilizadores,
            'veiculos': veiculos,
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Registrar novo cliente
def cliente_registar(request):
    try:
        # Obter os utilizadores e veículos
        utilizadores = readjson_utilizador()  # Função para obter utilizadores
        veiculos = readjson_veiculo()  # Função para obter veículos
        
        if request.method == 'POST':
            form = FormCliente(request.POST)
            if form.is_valid():
                # Se o formulário for válido, cria um novo cliente
                create_cliente(
                    id_utilizador=form.cleaned_data['id_utilizador'],
                    historico_compras=form.cleaned_data['historico_compras'],
                    interesse_veiculos=form.cleaned_data['interesse_veiculos']
                )
                return redirect('clientes_listar')  # Redireciona para a lista de clientes
            else:
                # Aqui mostramos os erros do formulário no log
                print("Erros do formulário:", form.errors)
                return HttpResponse("Formulário inválido")  # Se o formulário for inválido
        else:
            form = FormCliente()  # Exibe o formulário vazio

        return render(request, 'Clientes/registar.html', {
            'form': form,
            'utilizadores': utilizadores,
            'veiculos': veiculos
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")



# Atualizar cliente existente
def cliente_atualizar(request, id):
    try:
        cliente = readone_cliente(id)
        utilizadores = readjson_utilizador()
        veiculos = readjson_veiculo()
        
        if not cliente:
            return HttpResponse("Cliente não encontrado.")
        
        cliente = cliente[0]  # Primeiro item da lista
        
        if request.method == 'POST':
            form = FormCliente(request.POST)
            if form.is_valid():
                update_cliente(
                    id_cliente=id,
                    id_utilizador=form.cleaned_data['id_utilizador'],
                    historico_compras=form.cleaned_data['historico_compras'],
                    interesse_veiculos=form.cleaned_data['interesse_veiculos']  # Lista
                )
                return redirect("clientes_listar")
        else:
            form = FormCliente(initial={
                'id_utilizador': cliente['id_utilizador'],
                'historico_compras': cliente['historico_compras'],
                'interesse_veiculos': cliente['interesse_veiculos'],  # Deve ser uma lista
            })

        # Verifique os dados enviados ao template
        print(f"Utilizadores: {utilizadores}")
        print(f"Veículos: {veiculos}")
        print(f"Form: {form}")

        return render(request, 'Clientes/editar.html', {
            'form': form,
            'utilizadores': utilizadores,
            'veiculos': veiculos,
        })
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")





# Remover cliente
from django.contrib import messages

def cliente_remover(request, id):
    try:
        remover_cliente(id)
        return redirect("cliente_listar")
    except RuntimeError as e:
        cliente = readjson_cliente()
        return render(request, 'clientes/listar.html', {'clientes': cliente, 'erro': str(e)})




