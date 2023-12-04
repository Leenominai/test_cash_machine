from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.views import CashMachineView, QRCodeFileView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("cash_machine", CashMachineView.as_view(), name="cash_machine"),
    path(
        "media/<str:file_name>/",
        QRCodeFileView.as_view(),
        name="qr_code_file",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
