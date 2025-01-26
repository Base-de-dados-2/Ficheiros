from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..Database.Transcao import (
    create_transacaovenda,
    update_transacaovenda,
    delete_transacaovenda,
    readone_transacaovenda,
    readjson_transacaovenda
)
from ..Formularios.transacao_form import FormTransacaoVenda
from ..Database.Transcao import readone_transacaovenda
from ..Database.Cliente import readjson_cliente
from ..Database.Veiculos import readjson_veiculo
from ..Database.Vendedor import readjson_vendedor

# Listar todas as transações de venda
def transacaovenda_listar(request):
    try:
        transacoes = readjson_transacaovenda()
        return render(request, 'Transação/listar.html', {'transacoes': transacoes})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Exibir detalhes de uma transação de venda
def transacaovenda_detalhes(request, id_transacao):
    try:
        # Obtém os dados da transação
        transacao = readone_transacaovenda(id_transacao)
        
        # Obtém os dados relacionados
        clientes = readjson_cliente()
        veiculos = readjson_veiculo()
        vendedores = readjson_vendedor()
        
        # Renderiza o template com os dados
        return render(request, 'Transação/detalhes.html', {
            'transacao': transacao,
            'clientes': clientes,
            'veiculos': veiculos,
            'vendedores': vendedores,
        })
    except Exception as e:
        return HttpResponse(f"Erro ao carregar os detalhes da transação: {e}")




# Registrar uma nova transação de venda
def transacaovenda_registrar(request):
    try:
        clientes = readjson_cliente()  # Lista de clientes
        veiculos = readjson_veiculo()  # Lista de veículos
        vendedores = readjson_vendedor()  # Lista de vendedores

        if request.method == 'POST':
            form = FormTransacaoVenda(request.POST)
            if form.is_valid():
                # Certifique-se de que existe uma função `create_transacaovenda`
                create_transacaovenda(
                    id_cliente=form.cleaned_data['id_cliente'],
                    id_veiculo=form.cleaned_data['id_veiculo'],
                    id_vendedor=form.cleaned_data['id_vendedor'],
                    data_venda=form.cleaned_data['data_venda'],
                    valor_venda=form.cleaned_data['valor_venda']
                )
                return redirect('transacaovenda_listar')  # Redireciona para a lista de transações
            else:
                print("Erros do formulário:", form.errors)
                return HttpResponse("Formulário inválido.")

        else:
            form = FormTransacaoVenda()

        return render(request, 'Transação/registar.html', {
            'form': form,
            'clientes': clientes,
            'veiculos': veiculos,
            'vendedores': vendedores,
        })

    except Exception as e:
        print(f"Erro ao registrar Transação de Venda: {e}")
        return HttpResponse(f"Ocorreu um erro: {e}")




# Atualizar uma transação de venda existente
def transacaovenda_atualizar(request, id_transacao):
    print(f"Debug: Iniciando atualização de transação. ID recebido: {id_transacao}")
    try:
        # Obtenha a transação
        transacao = readone_transacaovenda(id_transacao)
        print(f"Debug: Resultado de readone_transacaovenda({id_transacao}): {transacao}")

        # Verifica o tipo do retorno
        if not transacao:
            print("Debug: Transação não encontrada.")
            return HttpResponse("Transação de venda não encontrada.", status=404)

        if isinstance(transacao, dict):
            print("Debug: Transação retornada como dicionário.")
        elif isinstance(transacao, list) and len(transacao) > 0:
            transacao = transacao[0]
            print(f"Debug: Transação descompactada da lista: {transacao}")
        else:
            print(f"Debug: Formato inválido de transação: {transacao}")
            return HttpResponse("Transação de venda não encontrada ou dados inválidos.", status=404)

        if request.method == 'POST':
            print("Debug: Método POST recebido. Dados POST:")
            print(request.POST)

            form = FormTransacaoVenda(request.POST)
            if form.is_valid():
                print("Debug: Formulário válido. Dados limpos:")
                print(form.cleaned_data)
                try:
                    # Atualiza a transação
                    update_transacaovenda(
                        id_transacao=id_transacao,
                        id_cliente=form.cleaned_data['id_cliente'],
                        id_veiculo=form.cleaned_data['id_veiculo'],
                        id_vendedor=form.cleaned_data['id_vendedor'],
                        data_venda=form.cleaned_data['data_venda'],
                        valor_venda=form.cleaned_data['valor_venda']
                    )
                    print("Debug: Transação atualizada com sucesso.")
                    return redirect('transacaovenda_listar')
                except Exception as update_error:
                    print(f"Erro ao atualizar a transação: {update_error}")
                    return HttpResponse(f"Erro ao atualizar a transação: {update_error}", status=500)
            else:
                print("Debug: Formulário inválido. Erros:")
                print(form.errors)
        else:
            print("Debug: Método GET recebido. Preenchendo formulário com dados existentes.")
            # Preenche o formulário com os dados existentes
            form = FormTransacaoVenda(initial={
                'id_cliente': transacao.get('id_cliente'),
                'id_veiculo': transacao.get('id_veiculo'),
                'id_vendedor': transacao.get('id_vendedor'),
                'data_venda': transacao.get('data_venda'),
                'valor_venda': transacao.get('valor_venda'),
            })
            print("Debug: Formulário inicializado com dados:")
            print(form.initial)

        # Renderiza a página de edição
        return render(request, 'Transação/editar.html', {
            'form': form,
            'clientes': readjson_cliente(),
            'veiculos': readjson_veiculo(),
            'vendedores': readjson_vendedor(),
        })

    except KeyError as key_error:
        print(f"Erro de chave no dado da transação: {key_error}")
        return HttpResponse(f"Erro de chave no dado da transação: {key_error}", status=400)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return HttpResponse(f"Ocorreu um erro inesperado: {e}", status=500)



# Remover uma transação de venda
def transacaovenda_remover(request, id_transacao):
    try:
        delete_transacaovenda(id_transacao)
        return redirect('transacaovenda_listar')
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro ao remover a transação de venda: {e}")
