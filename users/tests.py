from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserRegistrationTest(APITestCase):

    def test_user_registration(self):
        url = reverse('users:register')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '+1234567890',
            'city': 'Test City'
        }
        response = self.client.post(url, data, format='json')

        # Проверяем, что запрос прошёл успешно
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что пользователь действительно создан
        user = User.objects.filter(email='testuser@example.com').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('testpassword123'))


class UserAuthenticationTest(APITestCase):

    def setUp(self):
        # Создаём пользователя для аутентификации
        self.user = User.objects.create(email="authuser@example.com")
        self.user.set_password('authpassword123')
        self.user.is_active = True
        self.user.save()

    def test_user_login(self):
        url = reverse('users:login')
        data = {
            'email': 'authuser@example.com',
            'password': 'authpassword123'
        }
        response = self.client.post(url, data, format='json')

        # Проверяем, что запрос прошёл успешно
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в ответе есть access и refresh токены
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        # Сначала получаем refresh токен
        login_url = reverse('users:login')
        data = {
            'email': 'authuser@example.com',
            'password': 'authpassword123'
        }
        login_response = self.client.post(login_url, data, format='json')
        refresh_token = login_response.data['refresh']

        # Затем обновляем access токен
        refresh_url = reverse('users:token_refresh')
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(refresh_url, refresh_data, format='json')

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)


class CreateSuperUserCommandTest(TestCase):

    def test_csu_command(self):
        # Перед выполнением команды проверяем, что пользователя нет
        exists = User.objects.filter(email='admin@example.com').exists()
        if not exists:
            # Выполняем команду
            call_command('csu')

            # Проверяем, что суперпользователь создан
            user = User.objects.get(email='admin@example.com')
            self.assertTrue(user.is_superuser)
            self.assertTrue(user.is_staff)
            self.assertTrue(user.is_active)
            self.assertTrue(user.check_password('123qwe'))
