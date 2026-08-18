from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Rol

User = get_user_model()

class RolTests(APITestCase):
    
    def setUp(self):
        # Creamos un usuario normal y un usuario administrador (superuser)
        self.user_normal = User.objects.create_user(username='normaluser', email='sebastiangomez3a@gmail.com', password='password123', is_staff=False)
        self.user_admin = User.objects.create_user(username='adminuser', email='joantttgo@gmail.com', password='password123', is_staff=True, is_superuser=True)
        
        #Generamos los tokens JWT para ambos
        self.token_normal = str(RefreshToken.for_user(self.user_normal).access_token)
        self.token_admin = str(RefreshToken.for_user(self.user_admin).access_token)
        
        # Obtenemos la URL del router (gracias al basename='roles' y la ruta 'api/', 
        # el nombre de la ruta generada es 'roles-list')
        self.url = reverse('roles-list')

    def test_no_token_unauthorized(self):
        #Verificar que si no se envía ningún token, se deniega el acceso
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_forbidden(self):
        #Verificar que un usuario autenticado pero sin permisos de admin reciba un 403 Forbidden
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_normal}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_and_create_roles(self):
        #Verificar que un administrador pueda listar y crear roles exitosamente."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        
        # Probar GET
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        # Probar POST 
        data = {
            "nombre": "Contabilidad",
            "descripcion": "Área encargada de las finanzas"
        }
        response_post = self.client.post(self.url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        
        # Verificamos que realmente se haya guardado en la base de datos
        self.assertEqual(Rol.objects.count(), 1)
        self.assertEqual(Rol.objects.get().nombre, "Contabilidad")
