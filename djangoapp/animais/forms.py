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
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control form-control-sm'})

        self.fields['nome_comum'].widget.attrs['placeholder'] = 'Escreva o nome popular do animal'
        self.fields['habitat_natural'].widget.attrs['placeholder'] = 'Escreva o habitat natural do animal'
        self.fields['tanque'].widget.attrs['placeholder'] = 'Selecione o tanque ao qual o animal pertence'
        #self.fields['tipo_sanguineo'].widget.attrs['placeholder'] = 'Digite o tipo sanguíneo do animal'
        self.fields['alimentacao'].widget.attrs['placeholder'] = 'Ex: Verduras, Carnes vermelhas, etc...'
        self.fields['observacoes'].widget.attrs['placeholder'] = 'Escreva observações desse animal, Ex: O animal tem histórico de doenças respiratorias, etc..'