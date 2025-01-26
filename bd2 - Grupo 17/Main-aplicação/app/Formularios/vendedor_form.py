from django import forms
from ..Database.Utilizador import readjson_utilizador

class FormVendedor(forms.Form):
    id_utilizador = forms.ChoiceField(label="Utilizador", required=True)
    cargo = forms.CharField(label="Cargo", max_length=100, required=True)
    vendas_realizadas = forms.IntegerField(label="Vendas Realizadas", required=True)

    def __init__(self, *args, **kwargs):
        super(FormVendedor, self).__init__(*args, **kwargs)
        # Aqui você precisa preencher o campo 'id_utilizador' com os IDs de utilizadores existentes
        self.fields['id_utilizador'].choices = [(u['id_utilizador'], u['nome']) for u in readjson_utilizador()]
