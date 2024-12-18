from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

from transcend.views import TranslationViewSet


schema_view = get_swagger_view(title="docs")
router = DefaultRouter()
router.register(r"translations", TranslationViewSet, basename="translations")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/docs/",
        schema_view,
    ),
]
