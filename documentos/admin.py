from django.contrib import admin
from .models import Documento, TipoDocumentoConfig

@admin.register(TipoDocumentoConfig)
class TipoDocumentoConfigAdmin(admin.ModelAdmin):
  list_display = ('tipo_documento', 'area_responsable')
  search_fields = ('tipo_documento', 'area_responsable__nombre')

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id','tipo_documento', 'area', 'estado', 'subido_por', 'subido_en', 'actualizado_en')
    list_filter = ('area', 'estado', 'tipo_documento')
    search_fields = ('descripcion', 'subido_por__username')