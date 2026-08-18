from django.contrib import admin
from .models import Tarea

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista principal de tareas
    list_display = ('id', 'area', 'estado', 'documento', 'creado_en', 'actualizado_en')
    
    # Filtros laterales útiles
    list_filter = ('creado_en',)
    
    # Barra de búsqueda para encontrar tareas por título o por el tipo de documento asociado
    search_fields = ('area', 'documento__tipo_documento')