from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from roles.models import Rol
from .models import TipoDocumentoConfig, Documento

User = get_user_model()

class DocumentoTests(APITestCase):
    
    def setUp(self):
        # 1. Creamos roles necesarios
        self.rol_usuario = Rol.objects.create(nombre="Usuario", descripcion="Rol de usuario común")
        self.rol_contabilidad = Rol.objects.create(nombre="Contabilidad", descripcion="Área contable")
        
        # 2. Creamos usuarios de prueba con sus respectivos roles
        self.user_comun = User.objects.create_user(
            username='usercomun', 
            email='comun@example.com', 
            password='password123', 
            rol=self.rol_usuario
        )
        self.user_contabilidad = User.objects.create_user(
            username='userconta', 
            email='conta@example.com', 
            password='password123', 
            rol=self.rol_contabilidad
        )
        
        # 3. Creamos una configuración de tipo de documento (ej: 'factura' va a 'Contabilidad')
        self.config_doc = TipoDocumentoConfig.objects.create(
            tipo_documento='factura',
            area_responsable=self.rol_contabilidad
        )
        
        # 4. Generamos tokens JWT
        self.token_comun = str(RefreshToken.for_user(self.user_comun).access_token)
        self.token_contabilidad = str(RefreshToken.for_user(self.user_contabilidad).access_token)
        
        # 5. Ruta del endpoint (basada en router.register(r'documentos', ...))
        self.url = reverse('documento-list')

    def test_non_user_role_cannot_upload_document(self):
        """Verifica que un usuario de otra área (ej: Contabilidad) NO pueda subir documentos (POST)."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_contabilidad}')
        
        archivo_falso = SimpleUploadedFile("factura.txt", b"contenido de prueba", content_type="text/plain")
        data = {
            "tipo_documento": "factura",
            "archivo": archivo_falso,
            "descripcion": "Factura de prueba"
        }
        
        response = self.client.post(self.url, data, format='multipart')
        # Debe denegarse porque solo el rol 'usuario' (o admin) puede hacer POST
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_role_can_upload_document(self):
        """Verifica que un usuario con el rol 'usuario' sí pueda subir un documento exitosamente."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_comun}')
        
        archivo_falso = SimpleUploadedFile("factura.txt", b"contenido de prueba", content_type="text/plain")
        data = {
            "tipo_documento": "factura",
            "archivo": archivo_falso,
            "descripcion": "Factura de prueba"
        }
        
        response = self.client.post(self.url, data, format='multipart')
        
        # Verificamos que se haya creado correctamente (201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verificamos que se haya guardado en la base de datos
        self.assertEqual(Documento.objects.count(), 1)
        # Verificamos que el área se haya asignado automáticamente por el TipoDocumentoConfig
        self.assertEqual(Documento.objects.get().area.nombre, "Contabilidad")
