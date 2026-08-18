from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status

User = get_user_model()


class StatusViewsTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        
        self.status = Status.objects.create(name="Новый")
        self.status2 = Status.objects.create(name="В работе")

    @staticmethod
    def get_message_texts(response):
        return [
            str(message)
            for message in get_messages(response.wsgi_request)
        ]

    def test_statuses_index_unauthenticated(self):
        """Проверка, что без авторизации перекидывает на логин"""
        response = self.client.get(reverse("statuses_index"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('statuses_index')}"
        )

    def test_statuses_index_authenticated(self):
        """Проверка доступа к списку статусов для залогиненных"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses_index"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Новый")
        self.assertContains(response, "В работе")

    def test_status_create(self):
        """Проверка успешного создания статуса"""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("status_create"),
            {"name": "Завершен"},
        )
        
        self.assertRedirects(response, reverse("statuses_index"))
        self.assertTrue(Status.objects.filter(name="Завершен").exists())
        self.assertIn(
            "Статус успешно создан",
            self.get_message_texts(response),
        )

    def test_status_update(self):
        """Проверка обновления существующего статуса"""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("status_update", args=[self.status.pk]),
            {"name": "Обновленный статус"},
        )
        
        self.assertRedirects(response, reverse("statuses_index"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Обновленный статус")
        self.assertIn(
            "Статус успешно изменен",
            self.get_message_texts(response),
        )

    def test_status_delete(self):
        """Проверка удаления статуса"""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("status_delete", args=[self.status.pk])
        )
        
        self.assertRedirects(response, reverse("statuses_index"))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        self.assertIn(
            "Статус успешно удален",
            self.get_message_texts(response),
        )
