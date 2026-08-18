from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Documento, TipoDocumentoConfig
from roles.models import Rol

class DocumentoSerializer(serializers.ModelSerializer):
    subido_por_username = serializers.ReadOnlyField(source='subido_por.username')
    area = serializers.SlugRelatedField(
        queryset=Rol.objects.all(),
        slug_field='nombre',
        required=False
    )
    class Meta:
        model = Documento
        fields = '__all__'
        read_only_fields = ('subido_por', 'subido_en', 'actualizado_en')

    def validate(self, attrs):
        # Si es una petición POST (Crear)
        if self.instance is None:
          if 'estado' in attrs:
              raise PermissionDenied("No puedes poner el estado")
          tipo_doc_enviado = attrs.get('tipo_documento').strip().capitalize()
          try:
              config = TipoDocumentoConfig.objects.get(tipo_documento=tipo_doc_enviado)
              attrs['area'] = config.area_responsable
          except TipoDocumentoConfig.DoesNotExist:
              raise PermissionDenied(f"No hay una área responsable para el tipo de documento: {tipo_doc_enviado}.")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['subido_por'] = request.user
        return super().create(validated_data)