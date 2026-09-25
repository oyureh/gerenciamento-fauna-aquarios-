from django import forms
from ficha_clinica.models import FichaClinicaModel, TratamentoTanqueModels
from tinymce.widgets import TinyMCE

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Campo que aceita múltiplos arquivos corretamente."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Se não veio nenhum arquivo, retorna lista vazia (campo não obrigatório)
        if not data:
            return []
        # Se veio um único arquivo (não é lista), transforma em lista
        if not isinstance(data, (list, tuple)):
            data = [data]
        result = []
        for item in data:
            result.append(super().clean(item, initial))
        return result


class FichaClinicaForms(forms.ModelForm):

    arquivos = MultipleFileField(required=False)

    observacoes = forms.CharField(
        required=False,
        widget=TinyMCE(attrs={'cols': 80, 'rows': 20})
    )

    class Meta:
        model = FichaClinicaModel
        fields = [
            'animal',
            'data_entrada',
            'data_saida',
            'status',
            'motivo',
            'observacoes'
        ]

    def __init__(self, *args, **kwargs):
        self.animal_id = kwargs.pop('animal_id', None)
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-sm'
            })

        if self.instance and self.instance.pk:
            if self.instance.status == FichaClinicaModel.Status.FECHADA:
                for field in self.fields:
                    self.fields[field].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.pk:
            if self.instance.status == FichaClinicaModel.Status.FECHADA:
                raise forms.ValidationError(
                    "Esta ficha está fechada e não pode ser editada."
                )
        return cleaned_data

class TratamentoTanqueForms(forms.ModelForm):

    descricao = forms.CharField(
        required=False,
        widget=TinyMCE(attrs={'cols': 80, 'rows': 20})
    )
    class Meta:
        model  = TratamentoTanqueModels
        fields = ['tipo', 'titulo', 'status', 'responsavel', 'data_tratamento', 'descricao']
        widgets = {
            'data_tratamento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, TinyMCE):
                continue
            field.widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['titulo'].widget.attrs['placeholder']      = 'Ex: Limpeza semanal'
        self.fields['responsavel'].widget.attrs['placeholder'] = 'Responsável (opcional)'

        # Bloqueia os campos no HTML se o tratamento estiver FECHADO
        if self.instance and self.instance.pk:
            if self.instance.status == TratamentoTanqueModels.Status.FECHADA:
                for field in self.fields:
                    self.fields[field].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.pk:
            if self.instance.status == TratamentoTanqueModels.Status.FECHADA:
                raise forms.ValidationError("Este tratamento está fechado e não pode ser editado.")
        return cleaned_data