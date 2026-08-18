from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Documento
from tareas.models import Tarea

Usuario = get_user_model()

@receiver(post_save, sender=Documento)
def CrearTarea(sender, instance, created, **kwargs):
  if created:
    Tarea.objects.create(
        documento=instance,
        descripcion=f"Documento: {instance.tipo_documento}",
        area=instance.area,
        estado=instance.estado
    )

@receiver(post_save, sender=Documento)


def NotificarCorreo(sender, instance, created, **kwargs):
  if created:
    
    UsuariosArea = Usuario.objects.filter(rol = instance.area)
    CorreoDestino = [user.email for user in UsuariosArea if user.email]

    if CorreoDestino:
      asunto = f'Nuevo documento asignado: {instance.tipo_documento}'
      mensaje = f'Hola. Se ha subido un nuevo documento para tu area de {instance.area}.'
      remitente = settings.DEFAULT_FROM_EMAIL
      
      try:
          send_mail(
              subject=asunto,
              message=mensaje,
              from_email=remitente,
              recipient_list=CorreoDestino,
              fail_silently=False,
          )
          print(f"Correo enviado exitosamente a: {CorreoDestino} del area: {UsuariosArea[0].rol}")
      except Exception as e:
          print(f"Error al enviar el correo: {e}")