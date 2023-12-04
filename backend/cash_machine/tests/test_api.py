import datetime
import os

import pdfkit
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from receipts.models import Item


class CashMachineViewTest(APITestCase):
    """
    Тесты для проверки функциональности эндпоинта "cash_machine".

    Класс включает в себя тест для эндпоинта "cash_machine", который проверяет
    функциональность POST-запроса к данному эндпоинту. Предоставляет методы для
    установки начальных данных и завершения тестового класса.
    """

    @classmethod
    def setUpClass(cls):
        """
        Установка данных для всего класса тестов.

        Создаются тестовые объекты Item.

        Attributes:
            cls.item1 (Item): Тестовый объект товара.
            cls.item2 (Item): Тестовый объект товара.
            cls.item3 (Item): Тестовый объект товара.
        """
        super().setUpClass()
        cls.item1 = Item.objects.create(title="Item 1", price=10)
        cls.item2 = Item.objects.create(title="Item 2", price=20)
        cls.item3 = Item.objects.create(title="Item 3", price=30)

    def test_cash_machine_view(self):
        """
        Тест для проверки функциональности эндпоинта "cash_machine".

        Отправляет POST-запрос на эндпоинт с данными о товарах. Проверяет,
        что ответ имеет статус 200 OK и содержит изображение QR-кода.
        """
        data = {"items": [self.item1.id, self.item2.id, self.item3.id]}

        url = reverse("cash_machine")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("image/png", response["Content-Type"])

    @classmethod
    def tearDownClass(cls):
        """
        Завершение тестового класса.

        Удаляет созданный PDF-файл после выполнения всех тестов.
        """
        super().tearDownClass()
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%d.%m.%Y %H:%M")
        current_time = current_time.replace(":", "_").replace(" ", "_")

        pdf_file_path = f"media/check_{current_time}_1.pdf"
        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)


class QRCodeFileViewTest(APITestCase):
    """
    Тесты для проверки функциональности эндпоинта "qr_code_file".

    Класс включает в себя тест для эндпоинта "qr_code_file", который проверяет
    функциональность GET-запроса к данному эндпоинту. Предоставляет методы для
    установки начальных данных и завершения тестового класса.
    """

    def setUp(self):
        """
        Установка данных для теста.

        Загружает тестовый PDF-файл с использованием библиотеки pdfkit.
        """
        pdf_content = "This is a sample PDF content."
        self.pdf_file_path = os.path.join(settings.MEDIA_ROOT, "test_case.pdf")
        pdfkit.from_string(pdf_content, self.pdf_file_path)

    def test_qr_code_file_view(self):
        """
        Тест для проверки функциональности эндпоинта "qr_code_file".

        Отправляет GET-запрос на эндпоинт с указанием имени файла.
        Проверяет, что ответ имеет статус 200 OK, содержит изображение QR-кода
        и файл существует.
        """
        url_get = reverse(
            "qr_code_file", kwargs={"file_name": "test_case.pdf"}
        )
        response_get = self.client.get(url_get)

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        self.assertIn("application/pdf", response_get["Content-Type"])

        self.assertTrue(os.path.exists(self.pdf_file_path))

    @classmethod
    def tearDownClass(cls):
        """
        Завершение тестового класса.

        Удаляет созданный PDF-файл после выполнения всех тестов.
        """
        super().tearDownClass()
        pdf_file_path = "media/test_case.pdf"
        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)


class CreateItemsViewTest(APITestCase):
    """
    Тесты для проверки функциональности эндпоинта "api/v1/create_items/".
    """

    @classmethod
    def setUpClass(cls):
        """
        Установка данных для всего класса тестов.

        Создаются тестовые объекты Item.

        Attributes:
            cls.data = [
                {"id": 1, "title": "Макароны", "price": 80},
                {"id": 2, "title": "Огурцы", "price": 60},
                {"id": 3, "title": "Картошка", "price": 50}
            ]
        """
        super().setUpClass()
        cls.data = [
            {"id": 1, "title": "Макароны", "price": 80},
            {"id": 2, "title": "Огурцы", "price": 60},
            {"id": 3, "title": "Картошка", "price": 50},
        ]

    def test_create_items_view(self):
        """
        Тест для проверки функциональности эндпоинта "api/v1/create_items/".

        Отправляет POST-запрос на эндпоинт с данными о товарах. Проверяет,
        что ответ имеет статус 201 Created и содержит правильные id товаров.
        """
        url = reverse("create_items")
        response = self.client.post(url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.data
        self.assertIn("items", response_data)

        created_item_ids = response_data["items"]
        expected_item_ids = [item["id"] for item in self.data]
        self.assertEqual(created_item_ids, expected_item_ids)
