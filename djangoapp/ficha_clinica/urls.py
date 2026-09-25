from ficha_clinica.views import *
from django.urls import path

app_name = 'ficha_clinica'

urlpatterns = [
    path(
        'create/<int:pk>',
        CreateFichas.as_view(),
        name='create_ficha'   
    ),
    
    path(
        'update/<int:pk>',
        FichasUpdate.as_view(),
        name='update_ficha'   
    ),

    path(
        'detail/<int:pk>',
        DetailFichasview.as_view(),
        name='detail_ficha'   
    ),

    # ── Tratamentos ──
    path(
        'create/tratamento/<int:pk>',       # pk = tanque
        CreateTratamento.as_view(),
        name='create_tratamento'
    ),

    path(
        'update/tratamento/<int:pk>',       # pk = tratamento
        UpdateTratamento.as_view(),
        name='update_tratamento'
    ),

    path(
        'detail/tratamento/<int:pk>',       # pk = tratamento
        DetailTratamento.as_view(),
        name='detail_tratamento'
    ),
]