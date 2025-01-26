from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..Database.Veiculos import readjson_veiculo, create_veiculo, update_veiculo, readone_veiculo, readjson_veiculo_usados, remover_veiculo
from ..Formularios.veiculo_form import FormVeiculos

# Listar todos os veículos
def veiculos_listar(request):
    try:
        veiculos = readjson_veiculo()
        return render(request, 'veiculos/listar.html', {'veiculos': veiculos})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")
    
# Listar um único veículo baseado no ID
def veiculos_listar_id(request, id):
    try:
        veiculo = readone_veiculo(id)
        print(veiculo)  # Imprime o conteúdo de veiculo
        if veiculo:
            veiculo = veiculo[0]  # Acessa o primeiro item da lista
        return render(request, 'veiculos/listar_id.html', {'veiculo': veiculo})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")



# Listar veículos usados
def veiculos_usados(request):
    try:
        veiculos = readjson_veiculo_usados()
        return render(request, 'veiculos/listar_usados.html', {'veiculos': veiculos})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Registar um novo veículo
def veiculos_registar(request):
    try:
        if request.method == 'POST':
            form = FormVeiculos(request.POST)
            if form.is_valid():
                # Criar o veículo com os dados recebidos do formulário
                create_veiculo(
                    form.cleaned_data['marca'],
                    form.cleaned_data['modelo'],
                    form.cleaned_data['ano'],
                    form.cleaned_data['preco'],  # Preço do veículo
                    form.cleaned_data['quilometragem'],  # Quilometragem
                    form.cleaned_data['cor'],  # Cor
                    form.cleaned_data['tipo_combustivel'],  # Tipo de combustível
                    form.cleaned_data['id_stand'],  # ID do stand
                    form.cleaned_data['id_fornecedor']  # ID do fornecedor
                )
                return redirect("veiculos_listar")  # Redireciona para a lista de veículos
        else:
            form = FormVeiculos()  # Formulário vazio
        return render(request, 'veiculos/registar.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Atualizar um veículo existente
def veiculos_atualizar(request, id):
    try:
        # Carregar os dados do veículo usando a função readone_veiculo
        veiculos = readone_veiculo(id)  # Chama a função que já busca o veículo pelo ID

        if not veiculos:
            return HttpResponse("Veículo não encontrado.")  # Caso o veículo não seja encontrado
        
        veiculo = veiculos[0]  # Acessa o primeiro (e único) item da lista de veículos retornada

        # Depuração: exibir as chaves disponíveis no dicionário de veículo
        print("Chaves do veículo:", veiculo.keys())

        if request.method == 'POST':
            form = FormVeiculos(request.POST)
            if form.is_valid():
                # Atualiza o veículo no banco de dados com os dados do formulário
                update_veiculo(
                    id,  # ID do veículo a ser atualizado
                    marca=form.cleaned_data['marca'],
                    modelo=form.cleaned_data['modelo'],
                    ano=form.cleaned_data['ano'],
                    preco=form.cleaned_data['preco'],
                    quilometragem=form.cleaned_data['quilometragem'],
                    cor=form.cleaned_data['cor'],
                    tipo_combustivel=form.cleaned_data['tipo_combustivel'],  # Corrigido para 'tipo_combustivel'
                    id_stand=form.cleaned_data['id_stand'],
                    id_fornecedor=form.cleaned_data['id_fornecedor']
                )
                return redirect("veiculos_listar")  # Redireciona para a lista de veículos após atualização

        else:
            # Preenche o formulário com os dados do veículo
            # Exemplo ajustado, caso a chave seja diferente
            # Atualizar o preenchimento do formulário com a chave correta
            form = FormVeiculos(initial={
                'marca': veiculo['marca'],
                'modelo': veiculo['modelo'],
                'ano': veiculo['ano'],
                'preco': veiculo['preco'],
                'quilometragem': veiculo['quilometragem'],
                'cor': veiculo['cor'],
                'tipo_combustivel': veiculo.get('combustivel', ''),  # Corrigido para 'combustivel'
                'id_stand': veiculo['id_stand'],
                'id_fornecedor': veiculo['id_fornecedor']
            })

        return render(request, 'veiculos/editar.html', {'form': form})

    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

def veiculos_remover(request, id):
    try:
        # Tenta remover o veículo
        remover_veiculo(id)
        # Redireciona para a lista de veículos após a remoção
        return redirect("veiculos_listar")
    except RuntimeError as e:
        # Renderiza a lista de veículos com a mensagem de erro
        veiculos = readjson_veiculo()  # Assumindo que você tem uma função que retorna todos os veículos
        return render(request, 'veiculos/listar.html', {'veiculos': veiculos, 'erro': str(e)})
