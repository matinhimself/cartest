from django.test import TestCase

from .models import UserModel


# Create your tests here.

class TestPermission(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', password='12345')
        self.login = self.client.login(username='testuser', password='12345')
