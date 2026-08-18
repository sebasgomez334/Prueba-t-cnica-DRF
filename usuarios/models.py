from django.contrib.auth.models import AbstractUser
from django.db import models
from roles.models import Rol

class Usuario(AbstractUser):
    rol = models.ForeignKey(
        Rol, 
        on_delete=models.PROTECT,  # Evita que borren un rol si hay usuarios usándolo
        null=True,
        blank=True,
        related_name='usuarios'
    )
    email = models.EmailField('email address', unique=True)
  
    def __str__(self):
        return f"{self.username} - {self.rol}"