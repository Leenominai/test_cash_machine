import logging
import pytest

from rest_framework.test import APITestCase

from receipts.models import Item


logger = logging.getLogger(__name__)


@pytest.mark.django_db(transaction=True)
class ItemModelTest(APITestCase):
    """
    Класс тестов для проверки модели Item.

    Этот класс включает в себя тесты, проверяющие создание, получение, обновление и удаление
    элементов модели Item.
    """
    def setUp(self):
        """
        Установка данных для каждого теста.

        Создаются тестовые объекты Item.

        Attributes:
            self.item1 (Item): Тестовый объект товара.
            self.item2 (Item): Тестовый объект товара.
        """
        self.item1 = Item.objects.create(title="Компьютер", price=10000)
        self.item2 = Item.objects.create(title="Ноутбук", price=5000)

    def test_create_item_with_valid_data(self):
        """
        Проверяем, что создание элемента с корректными данными
        проходит успешно.
        """
        data = {"title": "Телефон", "price": 2000}
        item = Item.objects.create(**data)

        logger.info(f"Создан товар: {item.title} с идентификатором {item.id}")
        self.assertTrue(item.id > 0, "Элемент не был создан.")
        self.assertEqual(
            item.title,
            data["title"],
            "Название элемента не соответствует ожидаемому.",
        )
        self.assertEqual(
            item.price,
            data["price"],
            "Цена элемента не соответствует ожидаемой.",
        )

    def test_get_item_by_id(self):
        """
        Проверяем, что получение элемента по идентификатору
        проходит успешно.
        """
        item = Item.objects.get(id=self.item1.id)

        logger.info(f"Получен товар с идентификатором {item.id}")
        assert (
            item.id == self.item1.id
        ), "Идентификатор элемента не соответствует ожидаемому."
        assert (
            item.title == self.item1.title
        ), "Название элемента не соответствует ожидаемому."
        assert (
            item.price == self.item1.price
        ), "Цена элемента не соответствует ожидаемой."

    def test_get_items_list(self):
        """
        Проверяем, что получение списка элементов
        возвращает ожидаемый список.
        """
        items = Item.objects.all()

        logger.info(f"Получен список товаров: {[item.id for item in items]}")
        assert (
            len(items) == 2
        ), "Количество элементов не соответствует ожидаемому."
        assert (
            items[0].id == self.item1.id
        ), "Идентификатор первого элемента не соответствует ожидаемому."
        assert (
            items[0].title == self.item1.title
        ), "Название первого элемента не соответствует ожидаемому."
        assert (
            items[0].price == self.item1.price
        ), "Цена первого элемента не соответствует ожидаемой."
        assert (
            items[1].id == self.item2.id
        ), "Идентификатор второго элемента не соответствует ожидаемому."
        assert (
            items[1].title == self.item2.title
        ), "Название второго элемента не соответствует ожидаемому."
        assert (
            items[1].price == self.item2.price
        ), "Цена второго элемента не соответствует ожидаемой."

    def test_update_item_data(self):
        """
        Проверяем, что обновление данных элемента
        проходит успешно.
        """
        new_title = "Новый компьютер"
        new_price = 20000

        self.item1.title = new_title
        self.item1.price = new_price
        self.item1.save()

        item = Item.objects.get(id=self.item1.id)

        logger.info(
            f"Обновлен товар: {item.title} с идентификатором {item.id}"
        )
        assert item.title == new_title, "Название элемента не было обновлено."
        assert item.price == new_price, "Цена элемента не была обновлена."

    def test_delete_item(self):
        """
        Проверяем, что удаление элемента
        проходит успешно.
        """
        item_count = Item.objects.count()

        Item.objects.get(id=self.item1.id).delete()

        logger.info(f"Товар с идентификатором {self.item1.id} удален")
        assert Item.objects.count() == item_count - 1, "Элемент не был удален."
