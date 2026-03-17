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
    
    nome_comum      = models.CharField      (max_length=100, blank=False, null=False)
    habitat_natural = models.CharField      (max_length=200, blank=True)
    tanque          = models.ForeignKey     (TanqueModels, on_delete=models.CASCADE, blank=False, null=False)
    data_criacao    = models.DateTimeField  (auto_now_add=True)
    alimentacao     = models.CharField      (max_length=250, blank=True, null=True)
    observacoes     = models.TextField      (blank=True, null=True)
    obito           = models.BooleanField   (default=False)
    foto            = models.ImageField     (upload_to='fotos_clientes/', blank=True, null=True)
    genero          = models.CharField      (max_length=30,  verbose_name='Sexo', blank=True, choices=GENERO_CHOICES, default='') 
    
    # Para modal
    
    def __str__(self):
        return self.nome_comum