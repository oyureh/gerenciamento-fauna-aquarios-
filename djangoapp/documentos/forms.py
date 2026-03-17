from django import forms
from documentos.models import EnviarDocumentoModel

class EnviardocumentoForms(forms.ModelForm):
    class Meta:
        model = EnviarDocumentoModel
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control form-control-sm'})
        

