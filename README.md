# Django CRUD with PostgreSQL

A step-by-step guide to creating a Django REST API with PostgreSQL backend, JWT authentication, and CORS support.

## Table of Contents

* [Setup Project](#setup-project)
* [Install Dependencies](#install-dependencies)
* [Configure Django REST Framework](#configure-django-rest-framework)
* [Connect to PostgreSQL](#connect-to-postgresql)
* [Create App and Model](#create-app-and-model)
* [Migrate Database](#migrate-database)
* [Serializers](#serializers)
* [Routes and Views](#routes-and-views)
* [Test CRUD API](#test-crud-api)
* [Authentication](#authentication)
* [JWT Authentication](#jwt-authentication)
* [Testing JWT with Postman](#testing-jwt-with-postman)

---

## Setup Project

```bash
django-admin startproject DjangoRestApisPostgreSQL
cd DjangoRestApisPostgreSQL
```

Project structure:

```
DjangoRestApisPostgreSQL/
├── DjangoRestApisPostgreSQL/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

---

## Install Dependencies

```bash
pip install djangorestframework psycopg2 django-cors-headers djangorestframework-simplejwt drf-yasg
```

---

## Configure Django REST Framework

Add to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

---

## Connect to PostgreSQL

Update `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

---

## Create App and Model

```bash
python manage.py startapp tutorials
```

Update `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'tutorials.apps.TutorialsConfig',
]
```

### CORS Setup

```python
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', 'django.middleware.common.CommonMiddleware', ...]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ('http://localhost:8081',)
```

### Define Model (`tutorials/models.py`)

```python
from django.db import models

class Tutorial(models.Model):
    title = models.CharField(max_length=70, default='', blank=False)
    description = models.CharField(max_length=200, default='', blank=False)
    published = models.BooleanField(default=False)
```

---

## Migrate Database

```bash
python manage.py makemigrations tutorials
python manage.py migrate tutorials
```

---

## Serializers (`tutorials/serializers.py`)

```python
from rest_framework import serializers
from tutorials.models import Tutorial

class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ('id', 'title', 'description', 'published')
```

---

## Routes and Views

### URLs (`tutorials/urls.py`)

```python
from django.urls import path
from tutorials import views

urlpatterns = [
    path('api/tutorials', views.tutorial_list),
    path('api/tutorials/<int:pk>', views.tutorial_detail),
    path('api/tutorials/published', views.tutorial_list_published),
]
```

### Project URLs (`DjangoRestApisPostgreSQL/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tutorials.urls')),
]
```

---

## Test CRUD API

```bash
python manage.py runserver 8080
```

**Admin Users**

* Admin: `admin` / `Hj923056!`
* User: `roger` / `hj923056`

---

## Authentication

* **SessionAuthentication:** Django sessions
* **BasicAuthentication:** username/password per request
* **TokenAuthentication:** static DB token
* **JWT:** recommended for modern APIs

---

## JWT Authentication

Add to `settings.py`:

```python
INSTALLED_APPS += ['rest_framework_simplejwt', 'drf_yasg']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}
```

Add JWT URLs:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

Views with JWT protection:

```python
class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [permissions.IsAuthenticated]
```

---

## Testing JWT with Postman

1. Create a user via Django admin.
2. POST to `http://127.0.0.1:8000/api/token/` with:

```json
{
  "username": "john",
  "password": "yourpassword"
}
```

3. Use returned `access` token for Authorization header:

```
Key: Authorization
Value: Bearer <access_token>
```

4. Refresh token if expired:

```bash
POST http://127.0.0.1:8000/api/token/refresh/
Body: { "refresh": "<your_refresh_token>" }
```
