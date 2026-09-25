from django.db import models

class TanqueModels(models.Model):
    TIPO_TANQUE_CHOICES = [
        ('DOCE', 'Água Doce'),
        ('SALGADA', 'Água Salgada'),
        ('SALOBRA', 'Água Salobra'),
        ('TERRESTRE', 'Terrestre'),
        ('AMBOS', 'Aquático & Terrestre'),    
    ]

    nome = models.CharField(max_length=125)
    tipo = models.CharField(max_length=10, choices=TIPO_TANQUE_CHOICES)    
    volume_litros = models.DecimalField(max_digits=10, decimal_places=2)
    temperatura_min = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperatura mínima em °C")
    temperatura_max = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperatura máxima em °C")
    ph_min = models.DecimalField(max_digits=4, decimal_places=2, help_text="pH mínimo")
    ph_max = models.DecimalField(max_digits=4, decimal_places=2, help_text="pH máximo")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class AnimaisModels(models.Model):
    GENERO_CHOICES = [
        ('FEMININO','FEMININO'),
        ('MASCULINO','MASCULINO'),
        ('OUTROS','OUTROS'),
    ]
    
    nome            = models.CharField      (max_length=100, blank=False, null=False)
    tanque          = models.ForeignKey     (TanqueModels, on_delete=models.CASCADE, blank=False, null=False)
    alimentacao     = models.CharField      (max_length=250, blank=True, null=True)
    observacoes     = models.TextField      (blank=True, null=True)
    pai             = models.CharField      (max_length=100, blank=True, null=True)
    mae             = models.CharField      (max_length=100, blank=True, null=True)
    
    obito           = models.BooleanField   (default=False)
    genero          = models.CharField      (max_length=30,  verbose_name='Sexo', blank=True, choices=GENERO_CHOICES, default='') 
    identificacao   = models.ForeignKey     ('IdentificacaoModels', on_delete=models.CASCADE, blank=False, null=False)

    data_de_nasc    =  models.DateField      (blank=True, null=True, verbose_name='Data de Nascimento')
    data_entrada    =  models.DateField      (blank=False, null=False, verbose_name='Data de Entrada')
    data_criacao    = models.DateTimeField  (auto_now_add=True)

    # Para modal
    
    def __str__(self):
        return self.nome
    
class IdentificacaoModels(models.Model):
    
    nome_identificacao = models.CharField(max_length=100, blank=False, null=False)
    
    def __str__(self):
        return self.nome_identificacao