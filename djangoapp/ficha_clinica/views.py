#Import Bibliotecas Django
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

# Importações locais
from ficha_clinica.models import FichaClinicaModel, FichaClinicaDocumentoModel, TratamentoTanqueModels
from ficha_clinica.forms import FichaClinicaForms, TratamentoTanqueForms
from animais.models import AnimaisModels, TanqueModels


class ListFichas(LoginRequiredMixin, ListView):
    model = FichaClinicaModel
    template_name = 'ficha/list_ficha.html'
    paginate_by = 13
    context_object_name = 'object_list'

    def get_queryset(self):
        animal_id = self.kwargs.get('pk') or self.kwargs.get('animal_id')
        if animal_id:
            return FichaClinicaModel.objects.filter(animal_id=animal_id).order_by('-data_entrada')
        return FichaClinicaModel.objects.all().order_by('-data_entrada')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_id = self.kwargs.get('pk') or self.kwargs.get('animal_id')
        if animal_id:
            context['animal'] = AnimaisModels.objects.filter(id=animal_id).first()
        return context


class DetailFichasview(LoginRequiredMixin, DetailView):
    model = FichaClinicaModel
    template_name = 'ficha/detail_ficha.html'
    context_object_name = 'ficha'


class CreateFichas(LoginRequiredMixin, CreateView):
    model = FichaClinicaModel
    form_class = FichaClinicaForms
    context_object_name = 'ficha'
    template_name = 'ficha/form_ficha.html'

    def get_animal(self):
        animal_id = self.kwargs.get('animal_id') or self.kwargs.get('pk')
        if animal_id:
            return AnimaisModels.objects.filter(id=animal_id).first()
        return None

    def dispatch(self, request, *args, **kwargs):
        animal = self.get_animal()
        if animal:
            ficha_aberta = FichaClinicaModel.objects.filter(
                animal=animal,
                status=FichaClinicaModel.Status.ABERTA
            ).exists()
            if ficha_aberta:
                # Redireciona de volta para o detalhe do animal com mensagem de erro
                return HttpResponseForbidden(
                    f"O animal '{animal}' já possui uma ficha clínica aberta. "
                    "Feche a ficha atual antes de criar uma nova."
                )
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        animal = self.get_animal()
        if animal:
            form.fields['animal'].initial = animal
            form.fields['animal'].widget.attrs['disabled'] = True
            form.fields['animal'].required = False
        return form

    def form_valid(self, form):
        animal = self.get_animal()
        if animal:
            form.instance.animal = animal
        self.object = form.save()
        files = form.cleaned_data.get('arquivos') or []
        for f in files:
            FichaClinicaDocumentoModel.objects.create(ficha=self.object, arquivo=f)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('animais:detail_animal', kwargs={'pk': self.object.animal_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animal'] = self.get_animal()
        return context


class FichasUpdate(LoginRequiredMixin, UpdateView):
    model = FichaClinicaModel
    form_class = FichaClinicaForms
    template_name = 'ficha/form_ficha.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status == FichaClinicaModel.Status.FECHADA:
            return HttpResponseForbidden("Esta ficha clínica foi fechada e não pode ser editada.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['animal'].widget.attrs['disabled'] = True
        form.fields['animal'].required = False
        return form

    def form_valid(self, form):
        form.instance.animal = self.get_object().animal
        response = super().form_valid(form)
        files = form.cleaned_data.get('arquivos') or []
        for f in files:
            FichaClinicaDocumentoModel.objects.create(ficha=self.object, arquivo=f)
        return response

    def form_invalid(self, form):
        print("FORM INVALID")
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('animais:detail_animais', kwargs={'pk': self.object.animal_id})
    

################### Tanques ###################
 

class ListFichas(LoginRequiredMixin, ListView):
    model = FichaClinicaModel
    template_name = 'ficha/list_ficha.html'
    paginate_by = 13
    context_object_name = 'object_list'

    def get_queryset(self):
        animal_id = self.kwargs.get('pk') or self.kwargs.get('animal_id')
        if animal_id:
            return FichaClinicaModel.objects.filter(animal_id=animal_id).order_by('-data_entrada')
        return FichaClinicaModel.objects.all().order_by('-data_entrada')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_id = self.kwargs.get('pk') or self.kwargs.get('animal_id')
        if animal_id:
            context['animal'] = AnimaisModels.objects.filter(id=animal_id).first()
        return context


class DetailFichasview(LoginRequiredMixin, DetailView):
    model = FichaClinicaModel
    template_name = 'ficha/detail_ficha.html'
    context_object_name = 'ficha'


class CreateFichas(LoginRequiredMixin, CreateView):
    model = FichaClinicaModel
    form_class = FichaClinicaForms
    context_object_name = 'ficha'
    template_name = 'ficha/form_ficha.html'

    def get_animal(self):
        animal_id = self.kwargs.get('animal_id') or self.kwargs.get('pk')
        if animal_id:
            return AnimaisModels.objects.filter(id=animal_id).first()
        return None

    def dispatch(self, request, *args, **kwargs):
        animal = self.get_animal()
        if animal:
            ficha_aberta = FichaClinicaModel.objects.filter(
                animal=animal,
                status=FichaClinicaModel.Status.ABERTA
            ).exists()
            if ficha_aberta:
                # Redireciona de volta para o detalhe do animal com mensagem de erro
                return HttpResponseForbidden(
                    f"O animal '{animal}' já possui uma ficha clínica aberta. "
                    "Feche a ficha atual antes de criar uma nova."
                )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        animal = self.get_animal()
        if animal:
            kwargs['animal_id'] = animal.pk
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        animal = self.get_animal()
        if animal:
            form.fields['animal'].initial = animal
            form.fields['animal'].widget.attrs['disabled'] = True
            form.fields['animal'].required = False
        return form

    def form_valid(self, form):
        animal = self.get_animal()
        if animal:
            form.instance.animal = animal
        self.object = form.save()
        files = form.cleaned_data.get('arquivos') or []
        for f in files:
            FichaClinicaDocumentoModel.objects.create(ficha=self.object, arquivo=f)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('animais:detail_animais', kwargs={'pk': self.object.animal_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animal'] = self.get_animal()
        return context


class FichasUpdate(LoginRequiredMixin, UpdateView):
    model = FichaClinicaModel
    form_class = FichaClinicaForms
    template_name = 'ficha/form_ficha.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status == FichaClinicaModel.Status.FECHADA:
            return HttpResponseForbidden("Esta ficha clínica foi fechada e não pode ser editada.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['animal'].widget.attrs['disabled'] = True
        form.fields['animal'].required = False
        return form

    def form_valid(self, form):
        form.instance.animal = self.get_object().animal
        response = super().form_valid(form)
        files = form.cleaned_data.get('arquivos') or []
        for f in files:
            FichaClinicaDocumentoModel.objects.create(ficha=self.object, arquivo=f)
        return response

    def form_invalid(self, form):
        print("FORM INVALID")
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('animais:detail_animais', kwargs={'pk': self.object.animal_id})
    

################### Tanques ###################
 
class CreateTratamento(LoginRequiredMixin, CreateView):
    model      = TratamentoTanqueModels
    form_class = TratamentoTanqueForms
    template_name = 'tanque/form_tratamento.html'
 
    def dispatch(self, request, *args, **kwargs):
        tanque_id = self.kwargs.get('pk')
        tanque = TanqueModels.objects.filter(id=tanque_id).first()
        
        if tanque:
            # Verifica se já existe um tratamento aberto para este tanque
            tratamento_aberto = TratamentoTanqueModels.objects.filter(
                tanque=tanque,
                status=TratamentoTanqueModels.Status.ABERTA
            ).exists()
            
            if tratamento_aberto:
                messages.error(request, f"O tanque '{tanque.nome}' já possui um tratamento em andamento (Aberto).")
                return redirect('animais:detail_tanque', pk=tanque_id)
                
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.tanque_id = self.kwargs['pk']
        messages.success(self.request, 'Tratamento registrado com sucesso!')
        return super().form_valid(form)
 
    def get_success_url(self):
        # Redireciona de volta para o perfil do tanque pós-atualização
        return reverse_lazy('animais:detail_tanque', kwargs={'pk': self.object.tanque_id})
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanque'] = TanqueModels.objects.filter(id=self.kwargs['pk']).first()
        return context
 
 
class UpdateTratamento(LoginRequiredMixin, UpdateView):
    model      = TratamentoTanqueModels
    form_class = TratamentoTanqueForms
    template_name = 'tanque/form_tratamento.html'
 
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status == TratamentoTanqueModels.Status.FECHADA:
            messages.error(request, "Este tratamento foi fechado e não pode ser editado.")
            return redirect('ficha_clinica:detail_tratamento', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)
 
    def form_valid(self, form):
        messages.success(self.request, 'Tratamento atualizado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'animais:detail_tanque',
            kwargs={'pk': self.object.tanque.id}
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanque'] = self.object.tanque
        return context
    
class DetailTratamento(LoginRequiredMixin, DetailView):
    model = TratamentoTanqueModels
    template_name = 'tanque/detail_tratamento.html'
    context_object_name = 'tratamento'
 

 