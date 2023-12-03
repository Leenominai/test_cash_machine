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
from drf_spectacular.utils import extend_schema
from jinja2 import Environment, FileSystemLoader
from receipts.models import Item  # noqa
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .decorators import check_post_schema, qrcode_get_schema

logger = logging.getLogger(__name__)


@extend_schema(tags=["Чек - генерация QR-кода"])
@check_post_schema
class CashMachineView(APIView):
    @csrf_exempt
    def generate_html_content(self, items, total_price, current_time):
        """Генерирует HTML-код для чека."""
        html_content = render_to_string(
            "receipt.html",
            {
                "items": items,
                "total_price": total_price,
                "current_time": current_time,
            },
        )

        jinja_env = Environment(loader=FileSystemLoader(settings.BASE_DIR))
        template = jinja_env.from_string(html_content)

        rendered_html = template.render()

        logger.info("HTML-код успешно сгенерирован.")

        return rendered_html

    @csrf_exempt
    def create_pdf_receipt(self, current_time, rendered_html):
        """Создаёт чек в формате PDF."""

        # Получаем текущее время
        current_time = current_time.replace(":", "_").replace(" ", "_")

        # Получаем количество чеков с таким именем
        count = len(
            [
                f
                for f in os.listdir(settings.MEDIA_ROOT)
                if f.startswith(f"check_{current_time}")
            ]
        )

        # Формируем префикс для имени файла
        prefix = "_" + str(count + 1)

        pdfkit_options = {
            'page-size': 'A7',  # Размер страницы A7 соответствует стандартной ширине кассового чека
            'margin-top': '5mm',
            'margin-right': '5mm',
            'margin-bottom': '5mm',
            'margin-left': '5mm',
        }

        # Создаём файл чека
        pdf_file_path = f"media/check_{current_time}{prefix}.pdf"
        # pdfkit_config = pdfkit.configuration(
        #     wkhtmltopdf=settings.WKHTMLTOPDF_DOCKER_PATH
        # )
        pdfkit_config = pdfkit.configuration(
            wkhtmltopdf=settings.WKHTMLTOPDF_LOCAL_PATH
        )
        pdfkit.from_string(
            rendered_html, pdf_file_path, configuration=pdfkit_config, options=pdfkit_options
        )

        logger.info("Файл чека в формате .pdf успешно сгенерирован.")

        return pdf_file_path

    @csrf_exempt
    def create_qrcode_receipt(self, request, pdf_file_path):
        """Создаёт чек в формате QR-code."""

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

        logger.info("Файл чека в формате QR-кода успешно сгенерирован.")

        return img

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

            rendered_html = self.generate_html_content(
                items, total_price, current_time
            )

            pdf_file_path = self.create_pdf_receipt(
                current_time, rendered_html
            )

            # Пример: Создание QR-кода и сохранение его в media
            img = self.create_qrcode_receipt(request, pdf_file_path)

            # Подготовка ответа с изображением QR-кода
            response = HttpResponse(content_type="image/png")
            img.save(response, "PNG")

            logger.info("Ответ с изображением QR-кода успешно сформирован.")

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
    """
    Вьюсет для получения файла по его имени через сканирование QR-кода.

    Methods:
        get(self, request, file_name): Обработка GET-запроса. Возвращает файл в ответ на запрос.

    """

    @csrf_exempt
    def get(self, request, file_name):
        """
        Обработка GET-запроса для получения файла.

        Args:
            request (Request): Объект запроса Django.
            file_name (str): Имя файла, которое передается в URL.

        Returns:
            Response: Возвращает файл в ответ на запрос.

        Raises:
            Response: В случае ошибки возвращает соответствующий HTTP-ответ с сообщением об ошибке.
        """
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if os.path.exists(file_path):
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
