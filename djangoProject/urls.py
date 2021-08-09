"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from allauth.account.views import confirm_email
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_auth.views import PasswordResetConfirmView
from rest_framework import permissions
from api.views import *
from users.views import CustomRegisterView

# router = routers.DefaultRouter()
# router.register(r'q', QuestionViewSet)
# router.register(r'blog', BlogVewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
                  url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                      name='schema-json'),
                  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  url(r'^', include('django.contrib.auth.urls')),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('admin/', admin.site.urls),
                  path('api/', include("api.urls")),
                  path('users/', include("users.urls")),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  url(r'^rest-auth/', include('rest_auth.urls')),
                  url(r'^rest-auth/registration/', CustomRegisterView.as_view(), name='my_custom_registration'),
                  # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
                  url(r'^accounts/', include('allauth.urls')),
                  url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email,
                      name='account_confirm_email'),
                  # re_path(
                  #     r'^rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                  #     PasswordResetConfirmView.as_view(),
                  #     name='password_reset_confirm'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
