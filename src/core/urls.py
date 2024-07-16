from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    include,
    path,
)

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from core import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nurbolot@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

api = [
    path('auth/', include('apps.user.urls')),
    path('', include('apps.books.urls')),
]

urlpatterns = [
                  path('api/v1/', include(api)),
                  path(
                      'swagger/',
                      schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui',  # noqa
                  ),
                  path(
                      'redoc/',
                      schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc',  # noqa
                  ),
                  path('admin/', admin.site.urls),
              ]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # noqa

