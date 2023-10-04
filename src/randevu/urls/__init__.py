import debug_toolbar  # type: ignore
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

from randevu.views import HomePageView
from django.views.generic import TemplateView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v2',
      description="Randevu Backend API",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


def trigger_error(request):
    division_by_zero = 1 / 0


api = [
    path('v2/', include('randevu.urls.v2')),
]

urlpatterns = [
    path('api/', include(api)),
    path('superadmin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('sentry-debug/', trigger_error),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', HomePageView.as_view()),
]
