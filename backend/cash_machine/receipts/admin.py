from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Класс настройки административного интерфейса для модели Item.

    Attributes:
        list_display (tuple): Список полей модели,
        отображаемых в списке объектов в административном интерфейсе.
    """

    list_display = ("id", "title", "price")
