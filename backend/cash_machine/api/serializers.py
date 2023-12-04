from rest_framework import serializers

from receipts.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Item.

    Преобразует объекты Item в формат JSON и наоборот.
    """

    class Meta:
        model = Item
        fields = ["id", "title", "price"]


class BadRequestErrorSerializer(serializers.Serializer):
    """
    Сериализатор для ошибки "Bad Request".

    Используется для возврата сообщения об ошибке с HTTP-статусом 400.
    """

    detail = serializers.CharField(
        default="Error.",
        help_text="Сообщение об ошибке",
    )


class NotFoundErrorSerializer(serializers.Serializer):
    """
    Сериализатор для ошибки "Not Found".

    Используется для возврата сообщения об ошибке с HTTP-статусом 404.
    """

    detail = serializers.CharField(
        default="Not found.",
        help_text="Сообщение об ошибке",
    )


class InternalServerErrorSerializer(serializers.Serializer):
    """
    Сериализатор для ошибки "Internal Server Error".

    Используется для возврата сообщения об ошибке с HTTP-статусом 500.
    """

    detail = serializers.CharField(
        default="Internal server error.",
        help_text="Сообщение об ошибке",
    )
