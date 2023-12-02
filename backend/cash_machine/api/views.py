import datetime
import logging
import os

import pdfkit
import qrcode
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_list_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, extend_schema
from jinja2 import Environment, FileSystemLoader
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .decorators import check_post_schema, qrcode_get_schema
from receipts.models import Item  # noqa

logger = logging.getLogger(__name__)


@extend_schema(tags=["Чек - генерация QR-кода"])
@check_post_schema
class CashMachineView(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            items_ids = request.data.get("items", [])
            items = get_list_or_404(Item, id__in=items_ids)

            # Логика формирования чека
            total_price = 0
            items_data = []

            for item in items:
                item_data = {
                    "title": item.title,
                    "price": item.price,
                }
                total_price += item_data["price"]
                items_data.append(item_data)

            # Получаем текущее время в локальном часовом поясе
            current_time = datetime.datetime.now()

            # Форматируем текущее время
            current_time = current_time.strftime("%d.%m.%Y %H:%M")

            # Получаем HTML-код из Django-шаблона
            html_content = render_to_string(
                "receipt.html",
                {
                    "items": items,
                    "total_price": total_price,
                    "current_time": current_time,
                },
            )

            # Используем Jinja2 для рендеринга HTML-кода
            jinja_env = Environment(loader=FileSystemLoader(settings.BASE_DIR))
            template = jinja_env.from_string(html_content)

            rendered_html = template.render()

            # Пример: Сохранение чека в PDF
            pdf_file_path = f"media/check_{current_time.replace(':', '_').replace(' ', '_')}.pdf"
            pdfkit_config = pdfkit.configuration(
                wkhtmltopdf=settings.WKHTMLTOPDF_LOCAL_DOCKER_PATH
            )
            pdfkit.from_string(
                rendered_html, pdf_file_path, configuration=pdfkit_config
            )

            # Пример: Создание QR-кода и сохранение его в media
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"http://{request.get_host()}/{pdf_file_path}")
            qr.make(fit=True)

            # Преобразование QR-кода в PNG изображение
            img = qr.make_image(fill_color="black", back_color="white")

            # Подготовка ответа с изображением QR-кода
            response = HttpResponse(content_type="image/png")
            img.save(response, "PNG")
            return response

        except Http404 as e:
            logger.error(f"One or more items not found: {e}")
            return Response(
                {"error": "One or more items not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=["Чек - сканирование QR-кода"])
@qrcode_get_schema
class QRCodeFileView(APIView):
    @csrf_exempt
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="file_name", type=str, location=OpenApiParameter.PATH
            )
        ],
        responses={
            200: "application/pdf",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    def get(self, request, file_name):
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if os.path.exists(file_path):
                # Если файл существует, отправляем его как ответ
                return FileResponse(
                    open(file_path, "rb"), content_type="application/pdf"
                )
            else:
                return Response(
                    {"error": "File not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
