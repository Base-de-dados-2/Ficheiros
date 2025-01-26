from django import forms

class FormFornecedor(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contato = forms.CharField(label='Contato', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    veiculos_fornecedor = forms.CharField(label='Veiculos fornecidos', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
