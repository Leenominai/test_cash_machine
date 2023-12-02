from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from .views import CashMachineView, QRCodeFileView

urlpatterns = [
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("cash_machine", CashMachineView.as_view(), name="cash_machine"),
    path(
        "media/<str:file_name>/",
        QRCodeFileView.as_view(),
        name="qr_code_file",
    ),
]
