from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Tarea
from .serializers import TareaSerializer
from Empresa.permissions import OnlySuperCanDelete, OnlyPatchAndList

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes =[OnlyPatchAndList]
    
    def get_queryset(self):
      usuario = self.request.user

      if usuario.is_superuser:
        return Tarea.objects.all()
        
      if self.request.user.rol:
        return Tarea.objects.filter(
          area=usuario.rol,
          documento__estado='pendiente',
        )

      return Tarea.objects.none()