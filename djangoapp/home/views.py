# Imports Django / funções/ blib python
from django.views.generic import TemplateView
from animais.models import AnimaisModels, TanqueModels
from documentos.models import EnviarDocumentoModel

class Home(TemplateView):
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_tanques"] = TanqueModels.objects.count()
        context["animais_vivos"] = AnimaisModels.objects.filter(obito=False).count()
        context["animais_mortos"] = AnimaisModels.objects.filter(obito=True).count()
        context["documento_total"] = EnviarDocumentoModel.objects.count()

        return context
