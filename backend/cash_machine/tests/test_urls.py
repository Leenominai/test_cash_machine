import logging
import pytest

from http import HTTPStatus


logger = logging.getLogger(__name__)


@pytest.mark.django_db(transaction=True)
class TestAppURLs:
    """
    Класс тестов для проверки наличия
    и доступности URL-эндпоинтов в приложении.

    Этот класс включает в себя тесты, проверяющие наличие
    и доступность основных URL-эндпоинтов
    в административной панели Django.
    """

    def test_admin_url_exists_at_desired_location(self, client):
        """
        Проверяет, что эндпоинт `/admin/` доступен по ожидаемому URL.

        Args:
            client (Client): Django тестовый клиент.

        Returns:
            None
        """
        response = client.get("/admin/")
        assert (
            response.status_code == HTTPStatus.OK
            or response.status_code == HTTPStatus.FOUND
        ), (
            "Эндпоинт `/admin/` возвращает статус ответа, "
            "отличный от 200 или 302."
        )

        logger.info("Тест наличия эндпоинта `/admin/` выполнен успешно.")


@pytest.mark.django_db(transaction=True)
class TestAPIURL:
    """
    Класс тестов для проверки наличия и доступности API URL-эндпоинтов.

    Этот класс включает в себя тесты, проверяющие наличие
    и доступность URL-эндпоинтов, связанных с API,
    таких, как схема API, Swagger и Redoc.
    """

    def test_schema_url_exists_at_desired_location(self, client):
        """
        Проверяет, что эндпоинт `/api/v1/schema/` доступен по ожидаемому URL.

        Args:
            client (Client): Django тестовый клиент.

        Returns:
            None
        """
        response = client.get("/api/v1/schema/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/schema/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/schema/` возвращает ответ со статусом 200."
        )

        logger.info(
            "Тест наличия эндпоинта `/api/v1/schema/` выполнен успешно."
        )

    def test_swagger_url_exists_at_desired_location(self, client):
        """
        Проверяет, что эндпоинт `/api/v1/swagger-ui/`
        доступен по ожидаемому URL.

        Args:
            client (Client): Django тестовый клиент.

        Returns:
            None
        """
        response = client.get("/api/v1/swagger-ui/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/swagger-ui/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/swagger-ui/` возвращает ответ со статусом 200."
        )

        logger.info(
            "Тест наличия эндпоинта `/api/v1/swagger-ui/` выполнен успешно."
        )

    def test_redoc_url_exists_at_desired_location(self, client):
        """
        Проверяет, что эндпоинт `/api/v1/redoc/` доступен по ожидаемому URL.

        Args:
            client (Client): Django тестовый клиент.

        Returns:
            None
        """
        response = client.get("/api/v1/redoc/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/redoc/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/redoc/` возвращает ответ со статусом 200."
        )

        logger.info(
            "Тест наличия эндпоинта `/api/v1/redoc/` выполнен успешно."
        )
