from django.test import TestCase
# apps/users/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User

class UserAuthTests(APITestCase):
    def setUp(self):
        # بيانات التسجيل للمستخدم
        self.register_data = {
            "username": "testdoctor",
            "password": "strong-password-123",
            "password2": "strong-password-123",
            "email": "doctor@example.com",
            "first_name": "Test",
            "last_name": "Doctor",
            "role": User.Roles.DOCTOR
        }
        self.login_data = {
            "username": "testdoctor",
            "password": "strong-password-123"
        }

    def test_user_registration(self):
        """تأكد من أنه يمكن للمستخدم التسجيل بنجاح."""
        url = reverse('user_register')
        response = self.client.post(url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testdoctor')

    def test_user_login_and_token_obtain(self):
        """تأكد من أنه يمكن للمستخدم المسجل الحصول على توكن JWT."""
        # أولاً، قم بإنشاء المستخدم
        User.objects.create_user(
            username=self.login_data['username'],
            password=self.login_data['password']
        )
        
        # ثانياً، حاول تسجيل الدخول
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_access_protected_endpoint_with_token(self):
        """تأكد من إمكانية الوصول إلى مسار محمي باستخدام توكن صالح."""
        # قم بإنشاء المستخدم والحصول على التوكن
        User.objects.create_user(
            username=self.login_data['username'],
            password=self.login_data['password']
        )
        token_response = self.client.post(reverse('token_obtain_pair'), self.login_data, format='json')
        access_token = token_response.data['access']

        # قم بالوصول إلى المسار المحمي
        url = reverse('user_profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.login_data['username'])
    
    def test_access_protected_endpoint_without_token(self):
        """تأكد من رفض الوصول إلى مسار محمي بدون توكن."""
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        