import datetime
import logging
import os

import pdfkit
import qrcode
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, HttpRequest
from django.shortcuts import get_list_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .decorators import check_post_schema, qrcode_get_schema
from receipts.models import Item

logger = logging.getLogger(__name__)


@extend_schema(tags=["Чек - генерация QR-кода"])
@check_post_schema
class CashMachineView(APIView):
    """
    Эндпоинт для генерации QR-кода чека.

    Parameters:
        items (list): Список идентификаторов товаров, входящих в чек.

    Returns:
        HttpResponse: Изображение QR-кода, представленное в виде HTTP-ответа.

    Raises:
        Http404: Ошибка, если один или несколько товаров не найдены.
        Exception: В случае непредвиденной ошибки.

    Примечания:
        Данный эндпоинт принимает список идентификаторов товаров
        в теле POST-запроса и генерирует из них чек в формате PDF
        и соответствующий ему QR-код.

    Пример POST-запроса:
        {
            "items": [1, 2, 3]
        }
    """

    @csrf_exempt
    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Обработка POST-запроса для генерации QR-кода чека.

        Args:
            request (HttpRequest): Объект запроса,
            содержащий информацию о товарах.

        Returns:
            HttpResponse: Изображение QR-кода,
            представленное в виде HTTP-ответа.
        """
        try:
            items_ids = request.data.get("items", [])
            items = get_list_or_404(Item, id__in=items_ids)

            # Получаем текущее время в локальном часовом поясе
            current_time = datetime.datetime.now()

            # Форматируем текущее время
            current_time = current_time.strftime("%d.%m.%Y %H:%M")

            rendered_html = self.generate_html_content(items, current_time)

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
            logger.error(f"Один или несколько товаров не найдены: {e}")
            return Response(
                {"error": "Один или несколько товаров не найдены"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            logger.exception(f"Произошла непредвиденная ошибка: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @csrf_exempt
    def generate_html_content(self, items: list, current_time: str) -> str:
        """
        Генерирует HTML-код для чека.

        Args:
            items (list): Список объектов Item, представляющих товары в чеке.
            current_time (str): Текущее время, отформатированное в виде строки.

        Returns:
            str: Сгенерированный HTML-код для чека.

        Описание:
            Метод генерирует HTML-код для чека на основе переданных товаров
            и текущего времени. Для каждого товара создается словарь с
            информацией о нем, такой как название, цена,
            количество и общая стоимость товара.
            Затем эти данные передаются в шаблон "receipt.html",
            который использует Jinja2 для рендеринга HTML-кода.
            После успешной генерации ведется логирование события.
        """

        company_name = "ООО 'ОБЛАЧКО'"
        payment_method = "Наличными"
        customer_name = "Прекрасный покупатель"

        total_price = sum(item.price for item in items)

        items_data = []
        quantity = 1

        total_nds_price = total_price / 5

        for item in items:
            item_data = {
                "title": item.title,
                "price": item.price,
                "quantity": quantity,
                "total_item_price": item.price * quantity,
            }
            items_data.append(item_data)

        html_content = render_to_string(
            "receipt.html",
            {
                "items": items_data,
                "total_price": total_price,
                "total_nds_price": total_nds_price,
                "current_time": current_time,
                "company_name": company_name,
                "payment_method": payment_method,
                "customer_name": customer_name,
            },
        )

        jinja_env = Environment(loader=FileSystemLoader(settings.BASE_DIR))
        template = jinja_env.from_string(html_content)

        rendered_html = template.render()

        logger.info("HTML-код успешно сгенерирован.")

        return rendered_html

    @csrf_exempt
    def create_pdf_receipt(self, current_time: str, rendered_html: str) -> str:
        """
        Создаёт чек в формате PDF.

        Args:
            current_time (str): Текущее время, отформатированное в виде строки.
            rendered_html (str): Сгенерированный HTML-код для чека.

        Returns:
            str: Путь к созданному файлу чека в формате PDF.

        Описание:
            Метод создает чек в формате PDF на основе переданного времени
            и сгенерированного HTML-кода. Перед созданием файла проверяется
            количество файлов с аналогичным временем в имени,
            формируется уникальный префикс и указываются параметры
            для создания PDF с помощью библиотеки pdfkit. Файл сохраняется,
            и в случае успешной генерации происходит логирование события.
        """

        current_time = current_time.replace(":", "_").replace(" ", "_")

        count = len(
            [
                f
                for f in os.listdir(settings.MEDIA_ROOT)
                if f.startswith(f"check_{current_time}")
            ]
        )

        prefix = "_" + str(count + 1)

        pdfkit_options = {
            "page-size": "A7",
            "margin-top": "5mm",
            "margin-right": "5mm",
            "margin-bottom": "5mm",
            "margin-left": "5mm",
        }

        pdf_file_path = f"media/check_{current_time}{prefix}.pdf"
        # pdfkit_config = pdfkit.configuration(
        #     wkhtmltopdf=settings.WKHTMLTOPDF_DOCKER_PATH
        # )
        pdfkit_config = pdfkit.configuration(
            wkhtmltopdf=settings.WKHTMLTOPDF_LOCAL_PATH
        )
        pdfkit.from_string(
            rendered_html,
            pdf_file_path,
            configuration=pdfkit_config,
            options=pdfkit_options,
        )

        logger.info("Файл чека в формате .pdf успешно сгенерирован.")

        return pdf_file_path

    @csrf_exempt
    def create_qrcode_receipt(self, request: HttpRequest, pdf_file_path: str) -> Image:
        """
        Создаёт чек в формате QR-code.

        Args:
            request (HttpRequest): Объект запроса Django.
            pdf_file_path (str): Путь к файлу чека в формате PDF.

        Returns:
            Image: Объект изображения в формате PNG с содержимым QR-кода.

        Описание:
            Метод создает чек в формате QR-code, используя переданный запрос
            и путь к файлу чека. Для этого используется библиотека qrcode.
            Сформированный QR-код преобразуется в изображение
            с помощью библиотеки Pillow.
            После успешной генерации происходит логирование события.
        """

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


@extend_schema(tags=["Чек - сканирование QR-кода"])
@qrcode_get_schema
class QRCodeFileView(APIView):
    """
    Вьюсет для получения файла по его имени через сканирование QR-кода.

    Methods:
        get(self, request, file_name): Обработка GET-запроса.
        Возвращает файл в ответ на запрос.

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
            Response: В случае ошибки возвращает
            соответствующий HTTP-ответ с сообщением об ошибке.
        """
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    return FileResponse(file, content_type="application/pdf")
            else:
                return Response(
                    {"error": "File not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
