from django.db import models
from django.conf import settings
from usuarios.models import Usuario
from roles.models import Rol

class Documento(models.Model):
    ESTADO = (
            ('pendiente', 'Pendiente'),
            ('aceptado', 'Aceptado'),
            ('rechazado', 'Rechazado'),
    )
    area = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name='documentos'
    )
  
    tipo_documento = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='documentos/')
  
    estado = models.CharField(max_length=20, choices=ESTADO, default='pendiente')
    subido_por = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.PROTECT,
      related_name='documentos'
    )
    subido_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo_documento} - Área: {self.area}"

class TipoDocumentoConfig(models.Model):
  tipo_documento = models.CharField(max_length=20, unique=True) # Ej: 'factura'
  area_responsable = models.ForeignKey(Rol, on_delete=models.PROTECT) # Ej: Contabilidad

  def __str__(self):
    return f"{self.tipo_documento} -> {self.area_responsable}"
