from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('animais/', include('animais.urls', namespace='animais')),
    path('', include('login.urls', namespace='login')),
    path('documentos/', include('documentos.urls', namespace='documentos')),
    path('home/', include('home.urls', namespace='home'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
