from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from Empresa.permissions import OnlyCreateAndList, CanUploadDocument
from .models import Documento
from .serializers import DocumentoSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    tags=['Documentos'],
    description="Endpoint para la gestión de documentos con soporte para subida de archivos."
)
class DocumentoViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentoSerializer
    permission_classes = [OnlyCreateAndList, CanUploadDocument]
    parser_classes = (MultiPartParser, FormParser)
  
    def get_queryset(self):
      
      if self.request.user.is_superuser:
        return Documento.objects.all()

      if self.request.user.rol:
        # Solamente el area responsable y los pendientes
        return Documento.objects.filter(
          area=self.request.user.rol,
          estado='pendiente',
        )
        
      return Documento.objects.none()