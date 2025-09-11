from django.urls import include, path 
from tutorials import views 

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.routers import DefaultRouter
from .views import TutorialViewSet

router = DefaultRouter()
router.register(r'tutorials', TutorialViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="A description of your API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [ 
    # generate CRUD endpoints based on user defined ViewSet
    path('api/tutorials/', views.tutorial_list),
    path('api/tutorials/<int:pk>/', views.tutorial_detail),
    path('api/tutorials/published/', views.tutorial_list_published),
    
    # default CRUD methods (list, create, retrieve, update, partial_update, destroy)
    #path('api/', include(router.urls)), 
    
    # Swagger docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]