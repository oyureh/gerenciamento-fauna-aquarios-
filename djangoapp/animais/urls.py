from animais.views import *
from django.urls import path

app_name = 'animais'

urlpatterns = [
    path(
        'dashboard/', 
        Dashboard.as_view(), 
        name='dashboard'
    ),
    
    path(
        'update/tanque/<int:pk>',
        UpdateTanque.as_view(),
        name='update_tanque'   
    ),
    
    path(
        'delete/tanque/<int:pk>',
        DeleteTanque.as_view(),
        name='delete_tanque'   
    ),
    
    path(
        'create/tanque',
        CreateTanque.as_view(),
        name='create_tanque'   
    ),
    
    path(
        "export/tanques", 
        CreateTableView.as_view(), 
        name="Excel_tanque"
    ),
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    
    path(
        'list/animais', 
        ListAnimais.as_view(), 
        name='list_animais'
    ),
    
    path(
        'update/animais/<int:pk>',
        UpdateAnimais.as_view(),
        name='update_animais'   
    ),
    
    path(
        'delete/animais/<int:pk>',
        DeleteAnimais.as_view(),
        name='delete_animais'   
    ),
    
    path(
        'create/animais/<int:pk>',
        CreateAnimais.as_view(),
        name='create_animais'   
    ),
    
    path(
        'list/animais/<int:pk>',
        ListAnimaisTanqueEspecifico.as_view(),
        name='list_animais_tanque_especifico'
    ),
    
    path(
        "export/animais", 
        CreateTableAnimais.as_view(), 
        name="Excel_animais"
    ),
    
    path(
        'animal/<int:pk>/obito/', 
        ObitoBtnViews.as_view(), 
        name='obito_animal'
    ),
    
    path(
        'animal/<int:pk>/detail/', 
        Detailanimaisview.as_view(), 
        name='detail_animais'
    ),


    path(
        "ficha/medica/pdf/<int:pk>", 
        FichaMedicaPDFView.as_view(), 
        name="ficha_medica"
    ),
]
 