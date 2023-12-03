import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from receipts.models import Item


@pytest.mark.django_db
def test_create_item():
    item = Item.objects.create(title="Тестовый товар", price=10.99)
    assert item.id is not None
    assert str(item) == "Тестовый товар"


@pytest.mark.django_db
def test_title_max_length():
    with pytest.raises(ValidationError) as exc_info:
        item = Item.objects.create(title="A" * 256, price=10.99)
        item.full_clean()  # Явно вызываем валидацию
    assert "Ensure this value has at most 255 characters" in str(
        exc_info.value
    )


# @pytest.mark.django_db
# def test_price_max_digits():
#     with pytest.raises(ValidationError) as exc_info:
#         Item.objects.create(title="Тестовый товар", price=99999999999.99)
#     assert "Убедитесь, что в сумме не более 10 цифр" in str(exc_info.value)
#
#
# @pytest.mark.django_db
# def test_price_decimal_places():
#     with pytest.raises(ValidationError) as exc_info:
#         Item.objects.create(title="Тестовый товар", price=10.123)
#     assert "Убедитесь, что не более 2 десятичных знаков" in str(exc_info.value)
#
#
# @pytest.mark.django_db
# def test_unique_title():
#     Item.objects.create(title="Тестовый товар", price=10.99)
#     with pytest.raises(IntegrityError):
#         Item.objects.create(title="Тестовый товар", price=15.99)
