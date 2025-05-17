# AI Healthline API

AI Healthline is a Django-based RESTful API for managing tenant (clinic) authentication, including registration, login with OTP, email verification, password reset, and password change. This documentation provides setup instructions, endpoint details, and usage examples for developers and integrators.

---

## Table of Contents

-   [Features](#features)
-   [Tech Stack](#tech-stack)
-   [Getting Started](#getting-started)
-   [Environment Variables](#environment-variables)
-   [API Endpoints](#api-endpoints)
    -   [Tenant Signup](#1-tenant-signup)
    -   [Tenant Login](#2-tenant-login)
    -   [Get OTP](#3-get-otp)
    -   [Verify Email](#4-verify-email)
    -   [Password Reset Request](#5-password-reset-request)
    -   [Verify Password Reset Token](#6-verify-password-reset-token)
    -   [Confirm Password Reset](#7-confirm-password-reset)
    -   [Change Password](#8-change-password)
    -   [Logout](#9-logout)
-   [Authentication](#authentication)
-   [Error Handling](#error-handling)
-   [Contributing](#contributing)
-   [License](#license)

---

## Features

-   Tenant (clinic) registration with email verification
-   Secure login with OTP (One-Time Password) sent to email
-   Token-based authentication for protected endpoints
-   Password reset via email token
-   Password change for authenticated users
-   Logout functionality
-   Built with Django and Django REST Framework

---

## Tech Stack

-   Python 3.10+
-   Django 4.x
-   Django REST Framework
-   [two_factor](https://github.com/Bouke/django-two-factor-auth) (for OTP)
-   PostgreSQL

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/alx-cohort-4/healthline.git
cd healthline
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Apply Migrations

```sh
python manage.py migrate
```

### 5. Run the Development Server

```sh
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/v1/`

---

## Environment Variables

Create a `.env` file in the project root and configure the following (example):

```
TOP_KEY = ""
ENGINE = "django_multitenant.backends.postgresql"
DB_NAME = "AIAssistant"
DB_USER = "postgres"
DB_PASSWORD = "your database password"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
TOKEN_EXPIRATION = 5 # time in minutes
ALGO = "" # auth algorithm

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com" # 3 we will replace with the email server
EMAIL_PORT = 465
EMAIL_HOST_USER = "dummyaddress@dummy.com" # replace with the healthline email address
EMAIL_HOST_PASSWORD ="your-email-password"
EMAIL_USE_SSL = True

API_URL = "http://127.0.0.1:8080/"
```

---

## API Endpoints

### 1. Tenant Signup

-   **POST** `/api/v1/tenant/signup/`
-   Registers a new clinic/tenant.

**Request Body:**

```json
{
    "clinic_name": "Demo Clinic",
    "clinic_email": "demo@clinic.com",
    "website": "www.example.com",
    "country": "Nigeria",
    "address": "Ikeja, Lagos",
    "phonenumber": "+2348012345678",
    "password": "password123",
    "re_enter_password": "password123"
}
```

**Response:**

-   `200 OK` – Check your email for verification.

---

### 2. Tenant Login

-   **POST** `/api/v1/tenant/login/`
-   Logs in a tenant and sends an OTP to their email.

**Request Body:**

```json
{
    "clinic_email": "demo@clinic.com",
    "password": "password123"
}
```

**Response:**

-   `200 OK` – Check your email for OTP code.

---

### 3. Get OTP

-   **POST** `/api/v1/get-otp/`
-   Verifies the OTP sent to the user's email.

**Request Body:**

```json
{
    "clinic_email": "demo@clinic.com",
    "otp_code": "123456"
}
```

**Response:**

-   `202 Accepted` – Returns authentication token.

---

### 4. Verify Email

-   **GET** `/api/v1/tenant/verify-email/?token=<token>`
-   Verifies the tenant's email using a token sent via email.

**Response:**

-   `200 OK` – Returns clinic data and authentication token.

---

### 5. Password Reset Request

-   **POST** `/api/v1/tenant/password/reset/`
-   Sends a password reset token to the tenant's email.

**Request Body:**

```json
{
    "clinic_email": "demo@clinic.com"
}
```

**Response:**

-   `200 OK` – Check your email to continue.

---

### 6. Verify Password Reset Token

-   **GET** `/api/v1/tenant/verify-password-reset-token/?token=<token>`
-   Verifies the password reset token.

**Response:**

-   `200 OK` – Token is valid.

---

### 7. Confirm Password Reset

-   **POST** `/api/v1/tenant/password-reset/confirm/<clinic_email>/`
-   Resets the tenant's password.

**Request Body:**

```json
{
    "password": "newpassword123",
    "re_enter_password": "newpassword123"
}
```

**Response:**

-   `200 OK` – Returns authentication token.

---

### 8. Change Password

-   **POST** `/api/v1/tenant/verify-change-password/<clinic_email>/`
-   Changes the tenant's password. Requires authentication.

**Headers:**

```
Authorization: Token <your-auth-token>
```

**Request Body:**

```json
{
    "old_password": "oldpassword123",
    "new_password": "newpassword123",
    "confirm_new_password": "newpassword123"
}
```

**Response:**

-   `200 OK` – Password changed successfully.

---

### 9. Logout

-   **POST** `/api/v1/tenant/logout/`
-   Logs out the tenant and invalidates the token.

**Headers:**

```
Authorization: Token <your-auth-token>
```

**Response:**

-   `200 OK` – Successfully logged out.

---

## Authentication

-   The API uses **token-based authentication**.
-   After successful OTP verification or email verification, you will receive a token.
-   For protected endpoints, include the token in the `Authorization` header:

```
Authorization: Token <your-auth-token>
```

---

## Error Handling

-   All endpoints return appropriate HTTP status codes and error messages.
-   Common errors include invalid credentials, expired/invalid tokens, and missing fields.

---

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, please open an issue or contact the maintainer.
