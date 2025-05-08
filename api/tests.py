from django.test import TestCase
from django.urls import reverse
from tenant.models import TenantUser
from unittest.mock import patch
import jwt
import os
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

# Create your tests here.

class EmailVerificationTests(TestCase):
    def setUp(self):
        # Ensure all migrations are applied
        call_command('migrate')
        
        self.client = APIClient()
        # Create a test user
        self.test_user = TenantUser.objects.create(
            clinic_email="test@example.com",
            clinic_name="Test Clinic",
            website="www.example.com",
            country="Nigeria",
            phonenumber="+2348012345678",
            subscription="Basic",
            location="Ikeja, Lagos",
            password="testpass123",
            is_active=True,
            is_staff=False,
            email_verified=False
        )
        # Create and set authentication token
        self.token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Mock the JWT token
        self.valid_token = "valid_token"
        self.expired_token = "expired_token"
        self.invalid_token = "invalid_token"

    @patch('api.tasks.send_email.delay')
    def test_verify_email_success(self, mock_send_email):
        """Test successful email verification request"""
        url = reverse('verify_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Verification email sent."})
        mock_send_email.assert_called_once()

    @patch('api.tasks.send_email.delay')
    def test_verify_email_already_verified(self, mock_send_email):
        """Test email verification request for already verified email"""
        self.test_user.email_verified = True
        self.test_user.save()
        
        url = reverse('verify_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Email already verified."})
        mock_send_email.assert_not_called()

    @patch('jwt.decode')
    def test_verify_email_complete_success(self, mock_jwt_decode):
        """Test successful email verification completion"""
        mock_jwt_decode.return_value = {"sub": "test@example.com"}
        
        url = reverse('verify_email_complete')
        response = self.client.get(f"{url}?token={self.valid_token}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Email verified successfully"})
        
        # Verify user was updated
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.email_verified)

    @patch('jwt.decode')
    def test_verify_email_complete_expired_token(self, mock_jwt_decode):
        """Test email verification with expired token"""
        mock_jwt_decode.side_effect = jwt.ExpiredSignatureError()
        
        url = reverse('verify_email_complete')
        response = self.client.get(f"{url}?token={self.expired_token}")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Token has expired"})

    @patch('jwt.decode')
    def test_verify_email_complete_invalid_token(self, mock_jwt_decode):
        """Test email verification with invalid token"""
        mock_jwt_decode.side_effect = jwt.InvalidTokenError()
        
        url = reverse('verify_email_complete')
        response = self.client.get(f"{url}?token={self.invalid_token}")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Invalid token"})

    def test_verify_email_complete_nonexistent_user(self):
        """Test email verification for non-existent user"""
        # Create a token for a non-existent email
        non_existent_email = "nonexistent@example.com"
        with open('private.pem', 'r') as file:
            private_key = file.read()
        token = jwt.encode(
            payload={"sub": non_existent_email},
            key=private_key,
            algorithm=os.getenv("ALGO", "RS256")
        )
        
        url = reverse('verify_email_complete')
        response = self.client.get(f"{url}?token={token}")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Tenant does not exist"})
