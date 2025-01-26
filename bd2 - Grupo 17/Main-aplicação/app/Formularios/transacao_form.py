from django import forms
from ..Database.Cliente import readjson_cliente  # Função para obter os clientes existentes
from ..Database.Veiculos import readjson_veiculo  # Função para obter os veículos existentes
from ..Database.Vendedor import readjson_vendedor  # Função para obter os vendedores existentes

class FormTransacaoVenda(forms.Form):
    """Formulário para registrar ou atualizar uma transação de venda."""

    id_cliente = forms.ChoiceField(
        label="Cliente", 
        choices=[],  # As opções serão preenchidas dinamicamente com os clientes
        required=True
    )
    
    id_veiculo = forms.ChoiceField(
        label="Veículo", 
        choices=[],  # As opções serão preenchidas dinamicamente com os veículos
        required=True
    )
    
    id_vendedor = forms.ChoiceField(
        label="Vendedor", 
        choices=[],  # As opções serão preenchidas dinamicamente com os vendedores
        required=True
    )
    
    data_venda = forms.DateTimeField(
        label="Data da Venda", 
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), 
        required=True
    )
    
    valor_venda = forms.DecimalField(
        label="Valor da Venda", 
        max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={'placeholder': 'Digite o valor da venda'}), 
        required=True
    )

    def __init__(self, *args, **kwargs):
        # Chama o construtor da classe pai
        super(FormTransacaoVenda, self).__init__(*args, **kwargs)

        # Preenche os campos dinamicamente
        clientes = readjson_cliente()  # Pega os clientes existentes
        veiculos = readjson_veiculo()  # Pega os veículos existentes
        vendedores = readjson_vendedor()  # Pega os vendedores existentes

        # Preenche as opções para os clientes
        self.fields['id_cliente'].choices = [
            (cliente['id_cliente'], f"{cliente['id_cliente']} - {cliente['nome']}") for cliente in clientes
        ]

        # Preenche as opções para os veículos
        self.fields['id_veiculo'].choices = [
            (veiculo['id'], f"{veiculo['id']} - {veiculo['modelo']} ({veiculo['marca']})") for veiculo in veiculos
        ]

        # Preenche as opções para os vendedores
        self.fields['id_vendedor'].choices = [
            (vendedor['id_vendedor'], f"{vendedor['id_vendedor']} - {vendedor['nome']}") for vendedor in vendedores
        ]
