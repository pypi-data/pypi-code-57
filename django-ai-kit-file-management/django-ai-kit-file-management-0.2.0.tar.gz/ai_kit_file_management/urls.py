from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"files", views.FileViewSet, basename="file")

file_management_patterns = (
    [
        path(r"upload/", views.FileUploadView.as_view(), name="upload"),
        path(
            r"download/<str:uuid>/<str:filename>",
            views.FileDownloadView.as_view(),
            name="download",
        ),
    ]
    + router.urls,
    "ai_kit_file_management",
)

urlpatterns = [path("", include(file_management_patterns))]
