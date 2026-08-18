from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from roles.models import Rol

User = get_user_model()

class UserTests(APITestCase):
    
    def setUp(self):
        # 1. Creamos un Rol de prueba para asociarlo opcionalmente a los usuarios
        self.rol_admin = Rol.objects.create(nombre="Administrador", descripcion="Control total")
        
        # 2. Creamos un usuario normal y un usuario administrador
        self.user_normal = User.objects.create_user(
            username='normaluser', 
            email='normal@example.com', 
            password='password123', 
            is_staff=False
        )
        self.user_admin = User.objects.create_user(
            username='adminuser', 
            email='admin@example.com', 
            password='password123', 
            is_staff=True, 
            is_superuser=True,
            rol=self.rol_admin
        )
        
        # 3. Generamos los tokens JWT para ambos
        self.token_normal = str(RefreshToken.for_user(self.user_normal).access_token)
        self.token_admin = str(RefreshToken.for_user(self.user_admin).access_token)
        
        # 4. Definimos las URLs (gracias al basename='usuario' y la inclusión en api/, 
        # el listado usa 'usuario-list' y el login usa la ruta explícita)
        self.url_list = reverse('usuario-list')
        self.url_login = reverse('token_obtain_pair')

    def test_login_returns_custom_jwt_data(self):
        """Verifica que el login personalizado devuelva el token y los datos extra del usuario."""
        response = self.client.post(self.url_login, {
            "username": "adminuser",
            "password": "password123"
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('usuario', response.data)
        self.assertEqual(response.data['usuario']['username'], 'adminuser')
        self.assertEqual(response.data['usuario']['rol'], 'Administrador')

    def test_no_token_unauthorized(self):
        """Verifica que si no se envía token, se deniegue el acceso al listado de usuarios."""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_forbidden(self):
        """Verifica que un usuario sin privilegios de admin reciba un 403 Forbidden."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_normal}')
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_and_create_users(self):
        """Verifica que un administrador pueda listar y crear un nuevo usuario con su rol."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        
        # Probar GET (Listar)
        response_get = self.client.get(self.url_list)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        # Probar POST (Crear usuario nuevo)
        data = {
            "username": "nuevousuario",
            "email": "nuevo@example.com",
            "password": "securepassword123",
            "rol": "Administrador"
        }
        response_post = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        
        # Verificamos que se haya guardado correctamente
        self.assertEqual(User.objects.count(), 3)
