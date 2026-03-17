# Bibliotecas/funções python 
from django.views.generic import CreateView, ListView, DeleteView
from django.urls  import reverse_lazy
from django.contrib import messages

# Importe locais
from documentos.models import EnviarDocumentoModel
from documentos.forms import EnviardocumentoForms

class EnviarDocumentos(CreateView):
    model = EnviarDocumentoModel
    form_class = EnviardocumentoForms
    template_name = 'enviar_documento.html'
    success_url = reverse_lazy('documentos:lista_documentos')
    
    def form_invalid(self, form):
        # Adiciona as mensagens de erro ao sistema de mensagens
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class ListaDocumentos(ListView):
    model = EnviarDocumentoModel
    template_name = 'lista_documentos.html'
    ordering = ['titulo']
    # paginate_by = None
    # context_object_name = object_list
    
class DeleteDocumentos(DeleteView):
    model = EnviarDocumentoModel
    success_url = reverse_lazy('documentos:lista_documentos')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'O documento foi excluido com êxito' )
        # Chama o método delete da classe base para excluir o objeto
        return super().delete(request, **args, **kwargs)
    
    def form_invalid(self, form):
        # Adiciona as mensagens de erro ao sistema de mensagens
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)