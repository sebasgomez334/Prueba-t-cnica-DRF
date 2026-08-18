from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
      return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
      
class OnlySuperCanDelete(BasePermission):
    def has_permission(self, request, view):
      if request.method == 'DELETE':
        if not request.user or not request.user.is_superuser:
          raise PermissionDenied("Solo el superusuario tiene permitido eliminar documentos.")
      return True
      
class OnlyCreateAndList(BasePermission):
    def has_permission(self, request, view):
      if request.user and request.user.is_authenticated:
        AllowActions = ['create', 'list', 'retrieve']
        if view.action not in AllowActions:
          raise PermissionDenied("No puedes hacer esto")
        return True
        
class OnlyPatchAndList(BasePermission):
    def has_permission(self, request, view):
      if request.user and request.user.is_authenticated:
        AllowActions = ['partial_update', 'list', 'retrieve']
        if view.action not in AllowActions:
          raise PermissionDenied("No puedes hacer esto")
        return True

class CanUploadDocument(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
          
        if request.method == 'POST':
            if request.user.is_superuser:
                return True
            return request.user.rol and request.user.rol.nombre == 'Usuario'
            
        return False