from django.contrib import admin
from ficha_clinica.models import FichaClinicaModel, TipoTratamentoTanqueModels


class fichaAdmin(admin.ModelAdmin):
    pass
admin.site.register(FichaClinicaModel, fichaAdmin)

class TipoTratamentoTanqueAdmin(admin.ModelAdmin):  
    pass
admin.site.register(TipoTratamentoTanqueModels, TipoTratamentoTanqueAdmin)

    


