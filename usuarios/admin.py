from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Personalizamos la vista de administración para incluir nuestros campos nuevos
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff')

    search_fields = ('username', 'email', 'first_name', 'last_name', 'rol')

    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
          ('Rol', {'fields': ('rol',)}),
    )