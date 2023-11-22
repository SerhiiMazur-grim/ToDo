from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserApiViewSet, UserChangePasswordApiView


User = get_user_model()


class UserApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserApiViewSet.as_view({'get': 'list', 'get': 'retrieve', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})
        self.get_token_view = TokenObtainPairView.as_view()
        self.change_pass_view = UserChangePasswordApiView.as_view()
        
        self.user_1 = {
            'email': 'test_user_1@example.com',
            'first_name': 'F_name',
            'last_name': 'L_name',
            'password': 'testpassword',
            're_password': 'testpassword',
        }
        self.user_2 = {
            'email': 'test_user_2@example.com',
            'first_name': 'F_name',
            'last_name': 'L_name',
            'password': 'testpassword',
            're_password': 'testpassword',
        }
        self.admin = {
            'email': 'admin@example.com',
            'first_name': 'F_name',
            'last_name': 'L_name',
            'password': 'testpassword',
            're_password': 'testpassword',
        }
    

    def user_create(self, user_data):
        user = User.objects.create_user(
            user_data['first_name'],
            user_data['last_name'],
            user_data['email'],
            user_data['password'],
        )
        return user
    
    def admin_create(self, user_data):
        admin = User.objects.create_superuser(
            user_data['first_name'],
            user_data['last_name'],
            user_data['email'],
            user_data['password'],
        )
        return admin

    def user_token_resp(self, user):
        created_user = self.user_create(user)
        email = user['email']
        password = user['password']
        
        request = self.factory.post('/api/token/', {
            'email': email,
            'password': password,
        })
        response = self.get_token_view(request)
        
        return (created_user, response)
    
    def admin_token_resp(self, admin):
        created_admin = self.admin_create(admin)
        email = admin['email']
        password = admin['password']
        
        request = self.factory.post('/api/token/', {
            'email': email,
            'password': password,
        })
        response = self.get_token_view(request)
        
        return (created_admin, response)


    def test_create_user(self):
        request = self.factory.post('/users/', self.user_1)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.user_1['email'])
        self.assertEqual(response.data['is_superuser'], False)
    
    def test_false_create_user(self):
        req_fields = ['first_name', 'last_name', 'email', 'password', 're_password']
        false_user = {}
        request = self.factory.post('/users/', false_user)
        response = self.view(request)
        resp_fields = list(response.data.keys())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp_fields, req_fields)
    
    def test_false_re_password_create_user(self):
        false_user = self.user_1
        false_user['re_password'] = 'FalsePassword'
        request = self.factory.post('/users/', false_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_superuser(self):
        superuser = self.admin_create(self.admin)
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertEqual(superuser.is_superuser, True)
        
    def test_get_token(self):
        _, response = self.user_token_resp(self.user_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('refresh' in response.data.keys(), True)
        self.assertEqual('access' in response.data.keys(), True)
        
    def test_retrieve_user(self):
        user, response_token = self.user_token_resp(self.user_1)
        token = response_token.data.get("access")
        
        request = self.factory.get('/users/1/')
        force_authenticate(request, user=user, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
    
    def test_false_retrieve_user(self):
        self.user_create(self.user_1)
        user_2, response_token = self.user_token_resp(self.user_2)
        token = response_token.data.get("access")
        
        request = self.factory.get('/users/1/')
        force_authenticate(request, user=user_2, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            'You do not have permission to perform this action.',
            response.data['detail']
        )
    
    def test_admin_retrive_user(self):
        user = self.user_create(self.user_1)
        admin, response_token = self.admin_token_resp(self.admin)
        token = response_token.data.get("access")
        
        request = self.factory.get('/users/1/')
        force_authenticate(request, user=admin, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
    
    def test_method_put_false(self):
        user, response_token = self.user_token_resp(self.user_1)
        token = response_token.data.get("access")
        
        request = self.factory.put('/users/1/', self.user_2)
        force_authenticate(request, user=user, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_method_patch(self):
        user, response_token = self.user_token_resp(self.user_1)
        token = response_token.data.get("access")
        new_email = {'email': 'new_email@example.com'}
        
        request = self.factory.patch('/users/1/', new_email)
        force_authenticate(request, user=user, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], new_email['email'])
    
    def test_method_patch_by_admin_false(self):
        user = self.user_create(self.user_1)
        admin, response_token = self.admin_token_resp(self.admin)
        token = response_token.data.get("access")
        new_email = {'email': 'new_email@example.com'}
        
        request = self.factory.patch('/users/1/', new_email)
        force_authenticate(request, user=admin, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(user.email, new_email['email'])
    
    def test_delete_user_by_self(self):
        user, response_token = self.user_token_resp(self.user_1)
        token = response_token.data.get("access")
        
        request = self.factory.delete('/users/1/')
        force_authenticate(request, user=user, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        check_user = User.objects.filter(pk=1).exists()
        self.assertEqual(check_user, False)
    
    def test_delete_user_by_admin(self):
        self.user_create(self.user_1)
        admin, response_token = self.admin_token_resp(self.admin)
        token = response_token.data.get("access")
        
        request = self.factory.delete('/users/1/')
        force_authenticate(request, user=admin, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        check_user = User.objects.filter(pk=1).exists()
        self.assertEqual(check_user, False)
    
    def test_delete_user_by_another_user(self):
        self.user_create(self.user_1)
        user, response_token = self.user_token_resp(self.user_2)
        token = response_token.data.get("access")
        
        request = self.factory.delete('/users/1/')
        force_authenticate(request, user=user, token=token)
        response = self.view(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        check_user = User.objects.filter(pk=1).exists()
        self.assertEqual(check_user, True)
