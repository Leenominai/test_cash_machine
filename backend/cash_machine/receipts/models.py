from django.db import models


class Item(models.Model):
    """
    Модель для представления товара.

    Attributes:
        id (AutoField): Поле для автоматического присвоения уникальных идентификаторов.
        title (CharField): Поле для хранения названия товара.
        price (DecimalField): Поле для хранения цены товара с фиксацией десятичной части.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """
        Возвращает строковое представление товара.

        Returns:
            str: Строковое представление товара, в данном случае, используется название товара.
        """
        return self.title
