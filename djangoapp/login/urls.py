# from login.views import Login
# from django.urls import path

# app_name = 'login'

# urlpatterns = [
#     path(
#             '', 
#             Login.as_view(), 
#             name='login'
#         )
# ]  

from django.urls                import path
from . import views
from .views import CustomPasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView


app_name = 'login'

urlpatterns = [
    #Auth
    path('',        views.LoginView.as_view(),          name='login'),
    path('logout/', views.LogoutView.as_view(),         name='logout'),  

    #Usuário    
    path('configuracoes/permissoes/novo-usuario/',                 views.UserRegisterView.as_view(),       name='register'),
    path('configuracoes/permissoes/usuario-grupo/',                views.UserGroupHome.as_view(),          name='userGroupAndUserHome'), 
    path('configuracoes/permissoes/vincular-usuario-grupo/',       views.UserGroupLinkView.as_view(),      name='userGroupLink'),
    path('configuracoes/permissoes/desvincular-usuario-grupo/',    views.UserGroupUnlinkView.as_view(),    name='userGroupUnlink'),
    path('configuracoes/permissoes/<int:pk>/del/',                 views.UserDeleteView.as_view(),         name='userDelete'),    
    
    path(
        "trocar-senha/", 
        CustomPasswordChangeView.as_view(), 
        name="password_change")
    ,
    path(
        "trocar-senha/sucesso/", 
        PasswordChangeDoneView.as_view(template_name="accounts/novasenha/password_change_done.html"), 
        name="password_change_done"
    ),

    #Groups
    path('configuracoes/permissoes/novo-grupo/',                   views.GroupRegisterView.as_view()     , name='registerGroup'),
    # path('groups/new/',                 GroupCreateView.as_view()   , name='groupCreate'),
    # path('groups/<int:pk>/edit/',       GroupUpdateView.as_view()   , name='groupEdit'),
    path('configuracoes/permissoes/<int:pk>/del-gp/',              views.GroupDeleteView.as_view()   ,name='groupDelete'),

]