from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from task.models import Task
from users.models import User


class TaskTestCase(APITestCase):
    """Тест кейс для модели привычки"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.user2 = User.objects.create(email='test2@test.ru')
        self.task = Task.objects.create(action='Test action',
                                          place='Test place',
                                          time='19:00',
                                          pleasant_task=False,
                                          award='Test reward',
                                          is_public=True,
                                          duration=timedelta(minutes=1),
                                          owner=self.user)
        self.nice_task = Task.objects.create(action='Test enjoyable action',
                                               place='Test enjoyable place',
                                               time='19:00',
                                               pleasant_task=True,
                                               is_public=True,
                                               duration=timedelta(minutes=1),
                                               owner=self.user)

    def test_task_list_public(self):
        """Тест вывода списка публичных привычек"""
        url = reverse('task:tasks_public_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.all().count(), 2)

    def test_task_list_for_owner(self):
        """Тест вывода списка привычек определенного пользователя"""
        url = reverse('task:tasks_list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data.get('results')), 2)

    def test_task_retrieve(self):
        """Тест вывода одной привычки пользователя"""
        url = reverse('task:tasks_retrieve', args=(self.task.pk,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('id'), self.task.pk)

    def test_task_update(self):
        """Тест обновления привычки"""
        url = reverse('task:tasks_update', args=(self.task.pk,))
        data = {'action': 'Updated test action'}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('action'), 'Updated test action')

    def test_task_delete(self):
        """Тест удаления привычки"""
        url = reverse('task:tasks_delete', args=(self.task.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 1)

    def test_task_create(self):
        """Тест создания привычки"""
        url = reverse('task:tasks_create')
        data = {
            'place': 'Test place 2',
            'time': '19:00:00',
            'action': 'Test action 2',
            'pleasant_task': False,
            'periodicity': 1,
            'award': 'Test reward',
            'duration': '00:01:00',
            'is_public': True
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 3)
        self.assertEqual(response.json().get('action'), 'Test action 2')

        data_incorrect = {
            'place': 'Test place 2',
            'time': '19:00:00',
            'action': 'Test action 2',
            'pleasant_task': False,
            'periodicity': 1,
            'award': 'Test reward',
            'duration': '00:03:00',
            'is_public': True,
            'related_task': self.task.pk
        }
        response = self.client.post(url, data_incorrect)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json(), {'duration': ['Ensure this value is less than or equal to 0:02:00.'],})

        data_enjoyable_incorrect = {
            'place': 'Test place 2',
            'time': '19:00:00',
            'action': 'Test action 2',
            'pleasant_task': True,
            'periodicity': 1,
            'award': 'Test reward',
            'duration': '00:01:00',
            'is_public': True,
            'related_task': self.task.pk
        }
        response = self.client.post(url, data_enjoyable_incorrect)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)