from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from roles.models import Rol
from documentos.models import Documento
from .models import Tarea

User = get_user_model()

class TareaTests(APITestCase):
    
    def setUp(self):
        # 1. Creamos roles
        self.rol_contabilidad = Rol.objects.create(nombre="Contabilidad", descripcion="Área contable")
        self.rol_sistemas = Rol.objects.create(nombre="Sistemas", descripcion="Área técnica")
        
        # 2. Creamos usuarios de prueba
        self.user_conta = User.objects.create_user(
            username='userconta', 
            email='conta@example.com', 
            password='password123', 
            rol=self.rol_contabilidad
        )
        self.user_sistemas = User.objects.create_user(
            username='usersistemas', 
            email='sistemas@example.com', 
            password='password123', 
            rol=self.rol_sistemas
        )
        
        # 3. Creamos un documento (esto debería disparar la creación automática de su tarea correspondiente)
        self.documento = Documento.objects.create(
            area=self.rol_contabilidad,
            tipo_documento='factura',
            archivo='documentos/factura.txt',
            estado='pendiente',
            subido_por=self.user_conta
        )
        
        # 4. Obtenemos la tarea que se generó automáticamente para ese documento
        self.tarea = Tarea.objects.get(documento=self.documento)
        
        # 5. Generamos los tokens JWT
        self.token_conta = str(RefreshToken.for_user(self.user_conta).access_token)
        self.token_sistemas = str(RefreshToken.for_user(self.user_sistemas).access_token)
        
        # 6. Definimos las URLs
        self.url_list = reverse('tarea-list')
        self.url_detail = reverse('tarea-detail', kwargs={'pk': self.tarea.pk})

    def test_user_can_only_see_tasks_from_their_area_and_pending(self):
        """Verifica que un usuario de otra área no vea tareas ajenas, y que el de su área sí las vea."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_sistemas}')
        response_sistemas = self.client.get(self.url_list)
        self.assertEqual(response_sistemas.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_sistemas.data), 0)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_conta}')
        response_conta = self.client.get(self.url_list)
        self.assertEqual(response_conta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_conta.data), 1)

    def test_update_tarea_estado_updates_document(self):
        """Verifica que al actualizar el estado de la tarea mediante PATCH, este cambie en el documento asociado."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_conta}')
        
        data = {
            "estado": "aceptado"
        }
        
        response = self.client.patch(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.documento.refresh_from_db()
        self.assertEqual(self.documento.estado, "aceptado")
