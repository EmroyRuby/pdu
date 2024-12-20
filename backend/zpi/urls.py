"""
URL configuration for zpi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet, EventNotificationViewSet, EventRegistrationViewSet, \
    CategoryViewSet, CommentViewSet, GuestRegistrationAPIView, VerifyGuestRegistration, UserRecommendation
from zpi import settings

# from accounts.views import *

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'event-notifications', EventNotificationViewSet)
router.register(r'event-registrations', EventRegistrationViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="ZPI",
        default_version='v1',
        description="Zespolowe Przedsiewziecie Inzynierskie",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=([permissions.AllowAny]),
    authentication_classes=[SessionAuthentication]

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/accounts/', include('accounts.urls')),
    path('api/register-guest/', GuestRegistrationAPIView.as_view(), name='register-guest'),
    path('verify-guest-registration', VerifyGuestRegistration.as_view(), name='register-guest'),
    path('api/user-recommendation', UserRecommendation.as_view(), name='user-recommendation'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
