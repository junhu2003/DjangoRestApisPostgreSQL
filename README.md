Django CRUD with PostgreSQL overview

Install Django REST framework
pip install djangorestframework
Setup new Django project
django-admin startproject DjangoRestApisPostgreSQL
 
open settings.py and add Django REST framework to the INSTALLED_APPS array
INSTALLED_APPS = [
    ...
    # Django REST framework 
    'rest_framework',
]
Connect Django project to PostgreSQL
Python PostgreSQL adapter to PostgreSQL database
pip install psycopg2
setup PostgreSQL Database engine
open settings.py and change declaration of DATABASES:
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
Setup new Django app for Rest CRUD Api
cd DjangoRestApisPostgreSQL
python manage.py startapp tutorials
 
open tutorials/apps.py, modify TutorialsConfig class (subclass of django.apps.AppConfig)
add this new created app to DjangoRestApisPostgreSQL INSTALLED_APPS array in settings.py:
INSTALLED_APPS = [
    ...
    # Tutorials application 
    'tutorials.apps.TutorialsConfig',
]
Configure CORS
install the django-cors-headers library:
pip install django-cors-headers
In settings.py, add configuration for CORS:
INSTALLED_APPS = [
    ...
    # CORS
    'corsheaders',
]
also need to add a middleware class to listen in on responses:
MIDDLEWARE = [
    ...
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
Note: CorsMiddleware should be placed as high as possible, especially before any middleware that can generate responses such as CommonMiddleware.
Next, set CORS_ORIGIN_ALLOW_ALL and add the host to CORS_ORIGIN_WHITELIST:
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8081',
)
•	CORS_ORIGIN_ALLOW_ALL: If True, all origins will be accepted (not use the whitelist below). Defaults to False.
•	CORS_ORIGIN_WHITELIST: List of origins that are authorized to make cross-site HTTP requests. Defaults to [].
Define the Django Model
Open tutorials/models.py, add Tutorial class
from django.db import models
class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)
Migrate Data Model to PostgreSQL database
python manage.py makemigrations tutorials
To apply the generated migration, run the following Python script:
python manage.py migrate tutorials
Create Serializer class for Data Model
tutorials/serializers.py
from rest_framework import serializers 
from tutorials.models import Tutorial
 
 
class TutorialSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')
Define Routes to Views functions
These are our routes:
•	/api/tutorials: GET, POST, DELETE
•	/api/tutorials/:id: GET, PUT, DELETE
•	/api/tutorials/published: GET
Create a urls.py inside tutorials 
from django.urls import path 
from tutorials import views  
urlpatterns = [ 
    path('api/tutorials', views.tutorial_list),
    path('api/tutorials/<int:pk>', views.tutorial_detail),
    path('api/tutorials/published', views.tutorial_list_published),
]
Open DjangoRestApisPostgreSQL/urls.py
from django.contrib import admin
from django.urls import path, include
from tutorials import urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
]
Write API Views
Open tutorials/views.py and write following code


Test the CRUD with APIs
python manage.py runserver 8080

