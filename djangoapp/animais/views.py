# Importações de funções django
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, View, DetailView
from django.urls  import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.loader import get_template, render_to_string
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.staticfiles import finders

#Import Bibliotecas Django
import pandas as pd
import base64
import uuid
import datetime
from weasyprint import HTML

# Importações locais
from animais import urls
from animais.models import TanqueModels, AnimaisModels
from animais.forms import TanqueForms, AnimaisForms


def _logo_b64():
    path = finders.find('imgs/logo_acqua-removebg-preview.png')
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('ascii')
    return f'data:image/png;base64,{data}'

class Dashboard(LoginRequiredMixin, ListView):
    model = TanqueModels
    template_name = 'tanques/dashboard.html'
    ordering = ['nome']
    # paginate_by = None
    # context_object_name = object_list
    
    def get_queryset(self):
        queryset = super().get_queryset()
        busca = self.request.GET.get("q")

        if busca:
            busca = busca.strip()
            queryset = queryset.filter(
                Q(nome__icontains=busca) |
                Q(tipo__icontains=busca) |
                Q(data_criacao__icontains=busca) 
            )
        return queryset
    
class CreateTanque(LoginRequiredMixin, CreateView):
    model = TanqueModels
    form_class = TanqueForms
    success_url = reverse_lazy('animais:dashboard')
    template_name = 'tanques/form.html'
    
class UpdateTanque(LoginRequiredMixin, UpdateView):
    model = TanqueModels
    form_class = TanqueForms
    success_url = reverse_lazy('animais:dashboard')
    template_name = 'tanques/form.html'
    
class DeleteTanque(LoginRequiredMixin, DeleteView):
    model = TanqueModels
    success_url = reverse_lazy('animais:dashboard')
    
class CreateTableView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # 1. Buscar os dados do banco
        busca = request.GET.get("q")
        if busca:
            busca = busca.strip()
            queryset = TanqueModels.objects.filter(
                Q(nome__icontains=busca) |
                Q(tipo__icontains=busca) |
                Q(data_criacao__icontains=busca)
            ).values(
                'nome', 'tipo', 'volume_litros', 'temperatura_min',
                'temperatura_max', 'ph_min', 'ph_max'
            )
        else:
            queryset = TanqueModels.objects.all().values(
                'nome', 'tipo', 'volume_litros', 'temperatura_min',
                'temperatura_max', 'ph_min', 'ph_max'
            )

        # 2. Converter em DataFrame
        df = pd.DataFrame(list(queryset))

        # 3. Criar o HttpResponse configurado para Excel
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="Tanques.xlsx"'

        # 4. Salvar o DataFrame no HttpResponse
        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Tanques", index=False)

        return response

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

class ListAnimais(LoginRequiredMixin, ListView):
    model = AnimaisModels
    template_name = 'animais/list_animais.html'
    paginate_by = 13
    
    def get_queryset(self):
        queryset = super().get_queryset()
        busca = self.request.GET.get("q")
        status = self.request.GET.get("status")

        if busca:
            busca = busca.strip()
            queryset = AnimaisModels.objects.filter(
                Q(nome_comum__icontains=busca) |
                Q(tanque__nome__icontains=busca) |
                Q(tanque__data_criacao__icontains=busca)     
            )
            
        if status == "mortos":
            queryset = queryset.filter(obito=True)
        elif status == "vivos":
            queryset = queryset.filter(obito=False)
        return queryset
    
class ListAnimaisTanqueEspecifico(LoginRequiredMixin, ListView):
    model = AnimaisModels
    template_name = 'animais/list_animais.html'
    context_object_name = 'animais' # Garante que o template use o nome correto

    def get_queryset(self):
        # 1. Recupera o ID do tanque da URL
        tanque_id = self.kwargs.get('pk')
        
        # 2. Começa o queryset filtrando pelo tanque
        queryset = AnimaisModels.objects.filter(tanque_id=tanque_id)
        
        # 3. Recupera os parâmetros de busca da URL
        busca = self.request.GET.get("q")
        status = self.request.GET.get("status")

        # 4. Aplica filtros de busca, se existirem
        if busca:
            busca = busca.strip()
            queryset = queryset.filter(
                Q(nome_comum__icontains=busca) |
                Q(tanque__nome__icontains=busca) |
                Q(tanque__data_criacao__icontains=busca)     
            )
            
        # 5. Aplica filtros de status (mortos/vivos)
        if status == "mortos":
            queryset = queryset.filter(obito=True)
        elif status == "vivos":
            queryset = queryset.filter(obito=False)
            
        # IMPORTANTE: Removi o .values() para que o template receba OBJETOS 
        # e não dicionários. Se você usar .values(), não conseguirá acessar 
        # métodos do model ou campos relacionados facilmente no HTML.
        
        return queryset
    
class Detailanimaisview(LoginRequiredMixin, DetailView):
    model = AnimaisModels
    template_name = 'animais/detail_animais.html'
    context_object_name = 'animal'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        foto_base64 = request.POST.get('foto_base64')

        if foto_base64 and ';base64,' in foto_base64:
            # 1. Tratar a string Base64
            format, imgstr = foto_base64.split(';base64,')
            ext = format.split('/')[-1]
            
            # 2. Criar o arquivo em memória
            nome_arquivo = f"animal_{self.object.pk}_{uuid.uuid4().hex[:8]}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=nome_arquivo)

            # 3. Salvar no banco
            self.object.foto = data
            self.object.save()

        return redirect('animais:detail_animais', pk=self.object.pk)

   
class CreateAnimais(LoginRequiredMixin, CreateView):
    model = AnimaisModels
    form_class = AnimaisForms
    success_url = reverse_lazy('animais:list_animais')
    template_name = 'animais/form.html'
    
class UpdateAnimais(LoginRequiredMixin, UpdateView):
    model = AnimaisModels
    form_class = AnimaisForms
    success_url = reverse_lazy('animais:list_animais')
    template_name = 'animais/form.html'
    
class DeleteAnimais(LoginRequiredMixin, DeleteView):
    model = AnimaisModels
    success_url = reverse_lazy('animais:list_animais')
   
#   ++++++++++++++++++++++++++++++++++++ #

class FichaMedicaPDFView(DetailView):
    model = AnimaisModels

    def get(self, request, *args, **kwargs):
        # 1. Recupera o animal usando o método padrão da DetailView
        animal = self.get_object()
        
        # 2. Prepara o contexto para o template
        context = {
            'animal': animal,
            'data_emissao': datetime.datetime.now(),
            'logo_b64': _logo_b64()
        }

        # 3. Renderiza o HTML para uma string
        # CORREÇÃO: Use barras para frente '/' para evitar erro de escape no Windows (\f)
        try:
            html_string = render_to_string('pdf/ficha_animal.html', context)
        except Exception as e:
            return HttpResponse(f"Erro ao encontrar template: {e}", status=404)

        # 4. Configura o WeasyPrint
        # base_url permite encontrar imagens e CSS
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        
        # 5. Gera o binário do PDF
        pdf = html.write_pdf()

        # 6. Retorna a resposta como PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        
        # 'inline' abre no navegador. 'attachment' força o download.
        nome_arquivo = f"ficha_veterinaria_{animal.nome_comum}.pdf".replace(" ", "_")
        response['Content-Disposition'] = f'inline; filename="{nome_arquivo}"'
        
        return response
    
class ObitoBtnViews(View):
    def post(self, request, pk, *args, **kwargs):
        model = get_object_or_404(AnimaisModels, pk=pk)
        model.obito = not model.obito  # alterna True <-> False
        model.save()
        messages.success(request, f'O status do  "{model.nome_comum}" foi alterado.')
        return redirect(request.META.get('HTTP_REFERER', 'animais:list_animais'))

class CreateTableAnimais(LoginRequiredMixin, View):   
    def get(self, request, *args, **kwargs):
        busca = request.GET.get("q")
        status = request.GET.get("status")

        queryset = AnimaisModels.objects.all()

        if busca:
            busca = busca.strip()
            queryset = queryset.filter(
                Q(nome_comum__icontains=busca) |
                Q(habitat_natural__icontains=busca) |
                Q(tanque__nome__icontains=busca)
            )

        if status == "mortos":
            queryset = queryset.filter(obito=True)
        elif status == "vivos":
            queryset = queryset.filter(obito=False)

        queryset = queryset.values(
            'nome_comum', 'habitat_natural', 'tanque__nome'
        )

        df = pd.DataFrame(list(queryset))

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="Animais.xlsx"'

        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Animais", index=False)

        return response
