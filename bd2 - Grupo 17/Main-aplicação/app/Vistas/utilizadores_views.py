from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..Database.Utilizador import create_utilizador, update_utilizador, delete_utilizador, readjson_utilizador, readone_utilizador
from ..Formularios.utilizador_form import FormUtilizadores  # Formulário de utilizadores

# Listar todos os utilizadores
def utilizadores_listar(request):
    try:
        # Agora chamamos a função que busca os utilizadores do banco de dados
        utilizadores = readjson_utilizador()  # Essa função retorna uma lista de dicionários
    except Exception as e:
        print(f"Erro ao carregar utilizadores: {e}")
        utilizadores = []  # Garantir que a variável utilizadores não fique indefinida em caso de erro

    # Passando a variável 'utilizadores' para o template
    return render(request, 'utilizadores/listar.html', {'utilizadores': utilizadores})



# Função para listar um único utilizador baseado no ID   
def utilizadores_listar_id(request, id_utilizador):
    """Visualiza os detalhes de um utilizador pelo ID."""
    try:
        utilizador = readone_utilizador(id_utilizador)  # Função para obter um utilizador pelo ID
        return render(request, 'utilizadores/Listar_id.html', {'utilizador': utilizador})
    except Exception as e:
        return HttpResponse(f"Erro ao carregar o utilizador: {e}")




# Registar um novo utilizador
def utilizadores_registar(request):
    try:
        if request.method == 'POST':
            form = FormUtilizadores(request.POST)
            if form.is_valid():
                # Obter o valor do tipo_utilizador do formulário
                tipo_utilizador_num = form.cleaned_data['tipo_utilizador']
                
                # Convertendo o tipo_utilizador para "Admin" ou "Cliente" baseado no valor
                if tipo_utilizador_num == 1:
                    tipo_utilizador = 'Admin'
                elif tipo_utilizador_num == 0:
                    tipo_utilizador = 'Cliente'
                else:
                    # Se o valor não for 1 ou 0, define um valor padrão ou trata o erro
                    tipo_utilizador = 'Cliente'  # Pode alterar para o que preferir
                
                # Criar o utilizador com o tipo definido
                create_utilizador(
                    form.cleaned_data['nome'],
                    form.cleaned_data['email'],
                    form.cleaned_data['telefone'],
                    tipo_utilizador,  # Passando "Admin" ou "Cliente"
                    form.cleaned_data['data_criacao']
                )
                return redirect("utilizadores_listar")  # Redireciona para a lista de utilizadores
        else:
            form = FormUtilizadores()  # Formulário vazio
        return render(request, 'utilizadores/registar.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")



# Atualizar um utilizador existente
def utilizadores_atualizar(request, id):
    try:
        utilizador = readone_utilizador(id)
        if not utilizador:
            return HttpResponse("Utilizador não encontrado.")  # Caso o utilizador não seja encontrado
        
        if request.method == 'POST':
            form = FormUtilizadores(request.POST)
            if form.is_valid():
                update_utilizador(
                    id,
                    form.cleaned_data['nome'],
                    form.cleaned_data['email'],
                    form.cleaned_data['telefone'],
                    form.cleaned_data['tipo_utilizador'],
                    form.cleaned_data['data_criacao']
                )
                return redirect("utilizadores_listar")  # Redireciona para a lista de utilizadores após atualização
        else:
            form = FormUtilizadores(initial={
                'nome': utilizador['nome'],
                'email': utilizador['email'],
                'telefone': utilizador['telefone'],
                'tipo_utilizador': utilizador['tipo_utilizador'],
                'data_criacao': utilizador['data_criacao'],
            })

        return render(request, 'utilizadores/editar.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"Ocorreu um erro: {e}")

# Remover um utilizador
def utilizadores_remover(request, id):
    try:
        delete_utilizador(id)  # Tenta remover o utilizador
        return redirect("utilizadores_listar")  # Redireciona para a lista se a remoção for bem-sucedida
    except RuntimeError as e:
        # Renderiza a lista com uma mensagem de erro
        utilizadores = readjson_utilizador()
        return render(request, 'utilizadores/listar.html', {'utilizadores': utilizadores, 'erro': str(e)})




