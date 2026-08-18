from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Tarea
from documentos.models import Documento

class TareaSerializer(serializers.ModelSerializer):
    estado = serializers.CharField(required=False)
    documento_tipo = serializers.ReadOnlyField(source='documento.tipo_documento')

    class Meta:
        model = Tarea
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en',)
    
    def validate_estado(self, value):
        estados_validos = [estado[0] for estado in Documento.ESTADO]
        if value.strip().lower() not in estados_validos:
            raise PermissionDenied("Agrega un estado válido.")
        return value
      
    def validate(self, attrs):
        request = self.context.get('request')
        campos_enviados = set(attrs.keys())
        # Si es una petición PUT/PATCH (Actualizar)
        if self.instance:
          if campos_enviados - {'estado'}:
            raise PermissionDenied("Solo puedes cambiar el estado.")  
        return attrs
      
    def update(self, instance, validated_data):
        validated_data['estado'].strip().lower()
        return super().update(instance, validated_data)