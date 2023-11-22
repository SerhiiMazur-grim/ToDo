from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task


User = get_user_model()


class TaskApiTests(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            email='user_1@example.com',
            first_name='F_name',
            last_name='L_name',
            password='testpassword' 
        )
        self.user_2 = User.objects.create_user(
            email='user_2@example.com',
            first_name='F_name',
            last_name='L_name',
            password='testpassword'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            first_name='F_name',
            last_name='L_name',
            password='testpassword'
        )
        self.task_data_1_user_1 = {
            'owner': self.user_1,
            'title': 'task 1 title',
            'description': 'task 1 description',
            'done': False
        }
        self.task_data_2_user_1 = {
            'owner': self.user_1,
            'title': 'task 2 title',
            'description': 'task 2 description',
            'done': False
        }
        self.task_data_3_user_2 = {
            'owner': self.user_2,
            'title': 'task 3 title',
            'description': 'task 3 description',
            'done': False
        }
        self.task_data_4_user_2 = {
            'owner': self.user_2,
            'title': 'task 4 title',
            'description': 'task 4 description',
            'done': False
        }

    def api_authentication(self, user):
        token = str(RefreshToken.for_user(user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
    def create_tasks(self, *args):
        if len(args) == 1:
            result = Task.objects.create(**args[0])
        else:
            result = (Task.objects.create(**i) for i in args)
        
        return result


    def test_user_task_list(self):
        task_1, task_2 = self.create_tasks(self.task_data_1_user_1, self.task_data_2_user_1)
        self.api_authentication(self.user_1)
        response = self.client.get('/api/tasks/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], task_1.title)
        self.assertEqual(response.data[1]['title'], task_2.title)
    
    def test_user_task_list_false(self):
        self.create_tasks(self.task_data_1_user_1, self.task_data_2_user_1)
        self.api_authentication(self.user_2)
        response = self.client.get('/api/tasks/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_task(self):
        data = self.task_data_1_user_1
        del data['owner']
        self.api_authentication(self.user_1)
        response = self.client.post('/api/tasks/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_self_task(self):
        task = self.create_tasks(self.task_data_1_user_1)
        self.api_authentication(self.user_1)
        response = self.client.get(f'/api/tasks/{task.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)
    
    def test_retrieve_not_self_task(self):
        task = self.create_tasks(self.task_data_1_user_1)
        self.api_authentication(self.user_2)
        response = self.client.get(f'/api/tasks/{task.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_self_task(self):
        task = self.create_tasks(self.task_data_1_user_1)
        self.api_authentication(self.user_1)
        new_data = {
            'title': 'update task 1 title',
            'description': 'update task 1 description',
            'done': True
        }
        response = self.client.put(f'/api/tasks/{task.id}/', new_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_data['title'])
        self.assertEqual(response.data['description'], new_data['description'])
        self.assertEqual(response.data['done'], new_data['done'])
    
    def test_partial_update_self_task(self):
        task = self.create_tasks(self.task_data_1_user_1)
        self.api_authentication(self.user_1)
        part_update_data = {
            'title': 'update task 1 title'
        }
        response = self.client.patch(f'/api/tasks/{task.id}/', part_update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], part_update_data['title'])
        self.assertEqual(response.data['description'], task.description)
    
    def test_delete_self_task(self):
        task = self.create_tasks(self.task_data_1_user_1)
        self.api_authentication(self.user_1)
        response = self.client.delete(f'/api/tasks/{task.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_not_self_task(self):
        task = self.create_tasks(self.task_data_1_user_1)
        self.api_authentication(self.user_2)
        response = self.client.delete(f'/api/tasks/{task.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_not_self_task_by_admin(self):
        task = self.create_tasks(self.task_data_1_user_1)
        self.api_authentication(self.admin)
        response = self.client.delete(f'/api/tasks/{task.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_all_tasks_for_admin(self):
        self.create_tasks(
            self.task_data_1_user_1,
            self.task_data_2_user_1,
            self.task_data_3_user_2,
            self.task_data_4_user_2
        )
        self.api_authentication(self.admin)
        response = self.client.get(f'/api/tasks/all/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_all_tasks_for_user(self):
        self.create_tasks(
            self.task_data_1_user_1,
            self.task_data_2_user_1,
            self.task_data_3_user_2,
            self.task_data_4_user_2
        )
        self.api_authentication(self.user_1)
        response = self.client.get(f'/api/tasks/all/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
