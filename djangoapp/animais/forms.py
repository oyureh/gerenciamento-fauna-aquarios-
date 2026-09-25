from django import forms
from animais.models import TanqueModels, AnimaisModels

class TanqueForms(forms.ModelForm):
    class Meta:
        model = TanqueModels
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control form-control-sm'})
        
class AnimaisForms(forms.ModelForm):
    class Meta:
        model = AnimaisModels
        exclude = ['obito']

        widgets = {
            'data_de_nasc': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'data_entrada': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'genero': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm'
            })

        self.fields['identificacao'].widget.attrs.update({
            'placeholder': 'Selecione a identificação do animal'
        })

        self.fields['nome'].widget.attrs.update({
            'placeholder': 'Escreva o nome ou apelido do animal'
        })

        self.fields['alimentacao'].widget.attrs.update({
            'placeholder': 'Ex: Verduras, carnes, ração, etc...'
        })

        self.fields['observacoes'].widget.attrs.update({
            'placeholder': 'Observações gerais sobre o animal'
        })

        self.fields['pai'].widget.attrs.update({
            'placeholder': 'Nome do pai (opcional)'
        })

        self.fields['mae'].widget.attrs.update({
            'placeholder': 'Nome da mãe (opcional)'
        })
       