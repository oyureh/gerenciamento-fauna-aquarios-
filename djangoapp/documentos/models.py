from django.db import models

class EnviarDocumentoModel(models.Model):
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
    
    titulo      =   models.CharField(max_length=250, verbose_name='Título do documento')
    descricao   =   models.TextField(blank=True, null=True)
    documento   =   models.FileField(upload_to='documentos/')
    capa        =   models.FileField(upload_to='capas/')
    
    def __str__(self):
        return self.titulo
