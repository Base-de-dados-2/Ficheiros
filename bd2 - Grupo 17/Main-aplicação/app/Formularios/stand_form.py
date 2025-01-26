from django import forms

class FormStands(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    localizacao = forms.CharField(label='Localização', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    responsavel = forms.CharField(label='Responsável', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    def preencher_form(self, dados):
        """Preenche o formulário com os dados recebidos."""
        for key, value in dados.items():
            if key in self.fields:  # Certifique-se de que a chave existe no formulário
                self.fields[key].initial = value
