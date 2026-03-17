from documentos.views import *
from django.urls import path

app_name = 'documentos'

urlpatterns = [
    path(
            '', 
            ListaDocumentos.as_view(), 
            name='lista_documentos'
    ),
    
    path(
            'enviar/documento', 
            EnviarDocumentos.as_view(), 
            name='enviar_documentos'
    ),
    
    path(
            'delete/documento/<int:pk>/',
            DeleteDocumentos.as_view(),
            name="delete_documentos"
    ),
    
]  