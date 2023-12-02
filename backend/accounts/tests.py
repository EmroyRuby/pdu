from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import AppUser
from .validations import custom_validation, validate_email, validate_username, validate_password


# models tests


class AppUserModelTestCase(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )

    def test_create_user(self):
        self.assertIsInstance(self.user, AppUser)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.username, 'testuser')

    def test_create_superuser(self):
        superuser = AppUser.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpassword'
        )
        self.assertIsInstance(superuser, AppUser)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_str_method(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_email_required(self):
        with self.assertRaises(ValueError):
            AppUser.objects.create_user(
                email='',
                username='testuser3',
                password='testpassword3'
            )

    def test_user_manager_create_user(self):
        user = AppUser.objects.create_user(
            email='user@example.com',
            username='user',
            password='password'
        )
        self.assertIsInstance(user, AppUser)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_user_manager_create_superuser(self):
        superuser = AppUser.objects.create_superuser(
            email='admin2@example.com',
            username='admin2',
            password='admin2password'
        )
        self.assertIsInstance(superuser, AppUser)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

# views tests


User = get_user_model()


class UserViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client = APIClient()

    def test_user_register(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_user_login(self):
    #     url = reverse('login')
    #     data = {
    #         'email': 'test@example.com',
    #         'password': 'testpassword',
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_view(self):
        url = reverse('user')
        self.client.force_authenticate(user=self.user)  # Authenticate the test user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # validation tests


class ValidationTests(TestCase):
    def test_custom_validation(self):
        # Test with valid data
        data = {'email': 'test@example.com', 'username': 'testuser', 'password': 'testpassword'}
        result = custom_validation(data)
        self.assertEqual(result, data)

        # Test with an invalid password
        with self.assertRaises(ValidationError):
            data = {'email': 'new@example.com', 'username': 'newuser', 'password': 'short'}
            custom_validation(data)

    def test_validate_email(self):
        # Test with a valid email
        data = {'email': 'test@example.com'}
        result = validate_email(data)
        self.assertTrue(result)

        # Test with no email provided
        with self.assertRaises(ValidationError):
            data = {'email': ''}
            validate_email(data)

    def test_validate_username(self):
        # Test with a valid username
        data = {'username': 'testuser'}
        result = validate_username(data)
        self.assertTrue(result)

        # Test with no username provided
        with self.assertRaises(ValidationError):
            data = {'username': ''}
            validate_username(data)

    def test_validate_password(self):
        # Test with a valid password
        data = {'password': 'testpassword'}
        result = validate_password(data)
        self.assertTrue(result)

        # Test with no password provided
        with self.assertRaises(ValidationError):
            data = {'password': ''}
            validate_password(data)



