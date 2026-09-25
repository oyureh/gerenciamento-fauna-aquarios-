# ficha_clinica/models.py

from django.db import models
from django.utils import timezone
from animais.models import AnimaisModels, TanqueModels
from django.core.exceptions import ValidationError

class FichaClinicaModel(models.Model):

    class Status(models.TextChoices):
        ABERTA = "aberta", "Aberta"
        FECHADA = "fechada", "Fechada"

    class MotivoOcorrencia(models.TextChoices):
        TRATAMENTO = "tratamento", "Apenas Tratamento Médico"
        OBITO = "obito", "Óbito"
        TRANSFERENCIA = "transferencia", "Transferência"
        FUGA = "fuga", "Fuga"

    animal = models.ForeignKey(
        AnimaisModels,
        on_delete=models.PROTECT,
        related_name="fichas"
    )
    data_entrada = models.DateTimeField(
        default=timezone.now
    )
    data_saida = models.DateTimeField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTA
    )
    motivo = models.CharField(
        max_length=20,
        choices=MotivoOcorrencia.choices,
        default=MotivoOcorrencia.TRATAMENTO,
        verbose_name="Tipo de Ocorrência"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Tratamento Clínico / Observações"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    def clean(self):
        # Se a ficha já está salva no banco como FECHADA, impede qualquer alteração
        if self.pk:
            original = FichaClinicaModel.objects.get(pk=self.pk)
            if original.status == self.Status.FECHADA:
                raise ValidationError("Esta ficha clínica está fechada e não pode mais ser editada.")

    def save(self, *args, **kwargs):
        # Valida as regras antes de salvar
        self.full_clean()

        # Se fechou → preencher saída automaticamente
        if (
            self.status == self.Status.FECHADA
            and not self.data_saida
        ):
            self.data_saida = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal} - {self.get_motivo_display()} ({self.get_status_display()})"


# NOVA MODEL PARA MÚLTIPLOS DOCUMENTOS
class FichaClinicaDocumentoModel(models.Model):
    ficha = models.ForeignKey(
        FichaClinicaModel, 
        on_delete=models.CASCADE, 
        related_name="documentos"
    )
    arquivo = models.FileField(upload_to="fichas_clinicas/documentos/")
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc {self.id} - Ficha {self.ficha.id}"
    
# Adicione esta classe ao seu models.py existente

class TratamentoTanqueModels(models.Model):
    class Status(models.TextChoices):
        ABERTA = "aberta", "Aberto"
        FECHADA = "fechada", "Fechado"

    tanque          = models.ForeignKey(TanqueModels, on_delete=models.CASCADE, related_name='tratamentos')
    tipo            = models.ForeignKey("TipoTratamentoTanqueModels", on_delete=models.CASCADE, verbose_name='Tipo de Tratamento')
    titulo          = models.CharField(max_length=150, verbose_name='Título')
    descricao       = models.TextField(verbose_name='Descrição / Procedimento')
    responsavel     = models.CharField(max_length=100, blank=True, null=True, verbose_name='Responsável')
    data_tratamento = models.DateField(verbose_name='Data do Tratamento')
    data_criacao    = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    status          = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA, verbose_name='Status')

    class Meta:
        ordering = ['-data_tratamento', '-data_criacao']
        verbose_name = 'Tratamento'
        verbose_name_plural = 'Tratamentos'
    
    def clean(self):
        # Impede alteração se o tratamento já foi fechado no banco
        if self.pk:
            original = TratamentoTanqueModels.objects.get(pk=self.pk)
            if original.status == self.Status.FECHADA:
                raise ValidationError("Este tratamento de tanque está fechado e não pode mais ser editado.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.titulo} — {self.tanque.nome} ({self.get_status_display()}) ({self.data_tratamento})'
    
class TipoTratamentoTanqueModels(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name='Tipo de Tratamento')

    class Meta:
        verbose_name = 'Tipo de Tratamento'
        verbose_name_plural = 'Tipos de Tratamento'

    def __str__(self):
        return self.nome