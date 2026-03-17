# Importações locais
from django.contrib import messages
from django.views import View
from paciente import urls
from django.db.models import Q
from paciente.models import PersonModel, ConjugeModel
from paciente.forms import PersonForms, ConjugeForm

#Importações do Django
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView, TemplateView, View
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


# Importe de bibliotecas externas
from weasyprint import HTML
from django.core.files.base import ContentFile
import base64
import uuid

from agenda.models import Agendamento
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.decorators.http import require_GET
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from paciente.models import PersonModel
from storageR2.models import FileUpload
from storageR2.forms import FileUploadForm



            



#recebe a imagem via js e converte para base64
class PacienteFotoFormValidMixin:    
    def form_valid(self, form):
        
        foto_base64 = self.request.POST.get('foto_base64')        
        self.object = form.save(commit=False)

        if foto_base64:
            try:
               
                format, imgstr = foto_base64.split(';base64,') 
                ext = format.split('/')[-1] 
                data = ContentFile(base64.b64decode(imgstr))
                file_name = f"paciente_{self.object.cpf}_{uuid.uuid4().hex[:6]}.{ext}"
                self.object.foto.save(file_name, data, save=False)

            except (ValueError, TypeError):               
                pass 
        
        self.object.save()        
        form.save_m2m()    
        return super().form_valid(form)


class PacienteCreateView(LoginRequiredMixin, PacienteFotoFormValidMixin, CreateView):  
    model = PersonModel
    form_class = PersonForms
    template_name = 'paciente/form_person.html'      

    def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastro de Paciente'
        return context
    
    def get_success_url(self):
        return reverse_lazy('paciente:detail_person', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        # Adiciona as mensagens de erro ao sistema de mensagens
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class PacienteUpdateView(LoginRequiredMixin, PacienteFotoFormValidMixin, UpdateView):  
    model = PersonModel
    form_class = PersonForms
    template_name = 'paciente/form_person.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Atualização de Paciente'
        return context
    
    def get_success_url(self):
        return reverse_lazy('paciente:detail_person', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"O Paciente '{self.object}' foi atualizado com sucesso!")
        return response
    
    def form_invalid(self, form):
        # Adiciona as mensagens de erro ao sistema de mensagens
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class ListPerson(LoginRequiredMixin, ListView):
    model = PersonModel
    template_name = "paciente/list_person.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        busca = self.request.GET.get("q")

        if busca:
            busca = busca.strip()
            queryset = queryset.filter(
                Q(firstName__icontains=busca) |
                Q(lastName__icontains=busca) |
                Q(email__icontains=busca) |
                Q(telefoneCelular__icontains=busca) |
                Q(cpf__icontains=busca)
            )
        return queryset


class DetailPerson(LoginRequiredMixin, DetailView):
    model = PersonModel
    context_object_name = 'paciente'
    template_name = 'paciente/detail_person.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.object

        historico = (
            Agendamento.objects
            .select_related('medico', 'tipo_atendimento')  # ajuste nomes se forem diferentes
            .filter(paciente=paciente)
            .order_by('-data', '-horario')
        )
        context['historico'] = historico
        return context

    
class DeletePerson(LoginRequiredMixin, DeleteView):
    model = PersonModel
    success_url = reverse_lazy('paciente:list_person')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'O paciente foi excluido com êxito' )
        # Chama o método delete da classe base para excluir o objeto
        return super().delte(request, **args, **kwargs)
    
    def form_invalid(self, form):
        # Adiciona as mensagens de erro ao sistema de mensagens
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)
    

class CreateConjugue(LoginRequiredMixin, CreateView):
    model = ConjugeModel
    form_class = ConjugeForm
    template_name = 'paciente/form_conjugue.html'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Garante que o paciente vinculado exista antes de criar o cônjuge.
        O ID do paciente deve vir via URL: /paciente/<paciente_id>/conjuge/
        """
        self.paciente = get_object_or_404(PersonModel, pk=self.kwargs.get('paciente_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Vincula o cônjuge ao paciente automaticamente.
        """
        form.instance.paciente = self.paciente
        messages.success(self.request, f"Cônjuge de {self.paciente.firstName} cadastrado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redireciona para a tela de detalhes do paciente após o cadastro.
        """
        return reverse_lazy('paciente:detail_person', kwargs={'pk': self.paciente.pk})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

#####################################CONJUGE################################

# Paciente Pdf -------------------------------------------------------

class PacientePDFView(LoginRequiredMixin, DetailView):
    model = PersonModel
    # Não precisamos de um template HTML padrão, pois o PDF será servido
    # template_name = 'pacientes/detalhe.html' 
    def get(self, request, *args, **kwargs):
        # 1. Obter o objeto Paciente (a DetailView já faz isso, mas vamos refinar)
        paciente = self.get_object() 
        
        # 2. Renderizar o template HTML para o PDF
        # O nome do template será 'pacientes/relatorio_pdf.html' (vamos criá-lo no próximo passo)
        contexto = {
            'paciente': paciente,
        }
        
        # O template HTML que o WeasyPrint vai renderizar
        html_string = render_to_string('paciente/PDF.html', contexto)
        
        # 3. Gerar o PDF usando o WeasyPrint
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf_file = html.write_pdf()

        # 4. Configurar a resposta HTTP
        response = HttpResponse(pdf_file, content_type='application/pdf')
        
        # O cabeçalho 'Content-Disposition' força o download com o nome de arquivo desejado
        filename = f"Relatorio_Paciente_{paciente.firstName}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
    

###################### upload Files #######################


@require_GET
def view_file(request, pk: int):
    f = get_object_or_404(FileUpload, pk=pk)
    url = f.signed_url(expire=600, inline=True)  # 10min
    return redirect(url)



class PacienteFilesCreateView(LoginRequiredMixin, FormMixin, ListView):
    template_name = "paciente/paciente_doc_file.html"
    model = FileUpload
    context_object_name = "files"
    paginate_by = 12
    form_class = FileUploadForm

    # person vem da URL
    def dispatch(self, request, *args, **kwargs):
        self.person = get_object_or_404(PersonModel, pk=kwargs.get("person_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = FileUpload.objects.filter(person=self.person).order_by("-created_at")
        q  = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(name__icontains=q)
        # filtros extras (tipo, datas...), se tiver campos
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["patient"] = self.person
        ctx["form"] = ctx.get("form") or self.get_form()
        return ctx

    def get_success_url(self):  
        return reverse("paciente:paciente_files", kwargs={"person_id": self.person.pk})

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):      
        f = form.cleaned_data["file"] 

        try:            
            FileUpload.objects.create(
                person=self.person,
                name=f.name,
                file=f,
            )            
            messages.success(self.request, f"Arquivo '{f.name}' enviado com sucesso.")
        except Exception as e:
            messages.error(self.request, f"Falha ao enviar: {e}")
        
        return redirect(self.get_success_url())



class PacienteFileDownloadView(LoginRequiredMixin, ListView):
   
    def get(self, request, *args, **kwargs):
        file_id = kwargs.get("file_id")
        person_id = kwargs.get("person_id")
        obj = get_object_or_404(FileUpload, pk=file_id, person_id=person_id)        
        return HttpResponseRedirect(obj.signed_url(expire=900, inline=False)) # assina a bendita url para evitar vazamentos
    


class PacienteFileDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        file_id = kwargs.get("file_id")
        person_id = kwargs.get("person_id")
        obj = get_object_or_404(FileUpload, pk=file_id, person_id=person_id)        
        name = obj.name
        obj.delete()
        messages.success(request, f'"{name}" excluído.')
        return redirect(reverse("patient_files", kwargs={"person_id": person_id}))
