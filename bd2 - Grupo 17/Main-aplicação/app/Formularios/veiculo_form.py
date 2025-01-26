from django import forms
from ..Database.Stands import readjson_stand
from ..Database.Fornecedor import readjson_fornecedor

class FormVeiculos(forms.Form):
    marca = forms.CharField(label='Marca', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    modelo = forms.CharField(label='Modelo', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ano = forms.IntegerField(label='Ano', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    preco = forms.DecimalField(label='Preço', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    quilometragem = forms.IntegerField(label='Quilometragem', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cor = forms.CharField(label='Cor', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo_combustivel = forms.CharField(label='Tipo de Combustível', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Usando ChoiceField com opções dinâmicas dos stands
    id_stand = forms.ChoiceField(label='ID Stand', widget=forms.Select(attrs={'class': 'form-control'}))
    id_fornecedor = forms.ChoiceField(label='ID Fornecedor', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(FormVeiculos, self).__init__(*args, **kwargs)
        
        # Carregar os stands e fornecedores
        stands = readjson_stand()  # Obtemos todos os stands
        fornecedores = readjson_fornecedor()  # Obtemos todos os fornecedores
        
        # Preencher os campos de escolha
        self.fields['id_stand'].choices = [(stand['id_stand'], stand['nome']) for stand in stands]
        self.fields['id_fornecedor'].choices = [(fornecedor['id_fornecedor'], fornecedor['nome']) for fornecedor in fornecedores]
        
    def preencher_form(self, dados):
        """Preenche o formulário com os dados recebidos."""
        for key, value in dados.items():
            if key in self.fields:  # Certifique-se de que a chave existe no formulário
                self.fields[key].initial = value
