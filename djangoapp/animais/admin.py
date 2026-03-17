from django.contrib import admin
from animais.models import TanqueModels, AnimaisModels


class TanqueAdmin(admin.ModelAdmin):
    pass
admin.site.register(TanqueModels, TanqueAdmin)
    

class AnimaisAdmin(admin.ModelAdmin):
    pass
admin.site.register(AnimaisModels, AnimaisAdmin)

