from receipts.models import Item
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "title", "price"]


class BadRequestErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        default="Error.",
        help_text="Сообщение об ошибке",
    )


class NotFoundErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        default="Not found.",
        help_text="Сообщение об ошибке",
    )


class InternalServerErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        default="Internal server error.",
        help_text="Сообщение об ошибке",
    )
