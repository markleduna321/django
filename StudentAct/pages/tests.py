from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='pass12345!')
        self.client.force_login(self.user)

    def test_home_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_create_toggle_delete(self):
        response = self.client.post(reverse('task_create'), {'title': 'Study'})
        self.assertContains(response, 'Study')
        task = Task.objects.get()

        self.client.post(reverse('task_toggle', args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.is_done)

        self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertFalse(Task.objects.exists())

    def test_cannot_touch_other_users_task(self):
        other = User.objects.create_user('bob', password='pass12345!')
        task = Task.objects.create(user=other, title='Secret')
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 404)

    def test_register_logs_in(self):
        self.client.logout()
        response = self.client.post(reverse('register'), {
            'username': 'carol',
            'password1': 'Str0ng-pass-123',
            'password2': 'Str0ng-pass-123',
        })
        self.assertRedirects(response, reverse('home'))
