from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from documentos.models import Documento


class Tarea(models.Model):
    documento = models.OneToOneField(
        Documento, 
        on_delete=models.PROTECT, 
        related_name='tarea'
    )
    area = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
  
    @property
    def estado(self):
        return self.documento.estado

    @estado.setter
    def estado(self, nuevo_estado):
        self.documento.estado = nuevo_estado
        self.documento.save()

    def __str__(self):
        return f"Tarea para: {self.documento.area.nombre} - {self.area}"