from django import forms

class FormCliente(forms.Form):
    # Alterado para ChoiceField, semelhante ao campo 'interesse_veiculos'
    id_utilizador = forms.ChoiceField(
        label="Utilizador",
        choices=[],  # Será preenchido dinamicamente no __init__
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True  # Tornar esse campo obrigatório
    )
    
    historico_compras = forms.CharField(
        label="Histórico de Compras",
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        required=False
    )
    
    interesse_veiculos = forms.ChoiceField(  # Alterado para ChoiceField
        label="Interesse em Veículos",
        choices=[],  # Este será preenchido dinamicamente no `__init__`
        widget=forms.Select(attrs={'class': 'form-control'}),  # Usando Select para única escolha
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FormCliente, self).__init__(*args, **kwargs)
        
        # Preencher o campo 'id_utilizador' com os dados dos utilizadores
        from ..Database.Utilizador import readjson_utilizador  # Função para pegar utilizadores
        utilizadores = readjson_utilizador()
        self.fields['id_utilizador'].choices = [
            (utilizador['id_utilizador'], f"{utilizador['id_utilizador']} - {utilizador['nome']}")
            for utilizador in utilizadores
        ]
        
        # Preencher o campo 'interesse_veiculos' com os dados dos veículos
        from ..Database.Veiculos import readjson_veiculo  # Função para pegar os veículos
        veiculos = readjson_veiculo()
        self.fields['interesse_veiculos'].choices = [
            (
                veiculo['id'], 
                f"{veiculo['id']} - {veiculo['modelo']} ({veiculo['marca']})"
            ) 
            for veiculo in veiculos if 'id' in veiculo and 'modelo' in veiculo and 'marca' in veiculo
        ]
