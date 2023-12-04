from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestAppURLs:
    def test_admin_url_exists_at_desired_location(self, client):
        response = client.get("/admin/")
        assert response.status_code == HTTPStatus.OK or response.status_code == HTTPStatus.FOUND, (
            "Эндпоинт `/admin/` возвращает статус ответа, отличный от 200 или 302."
        )

    def test_cash_machine_url_exists_at_desired_location(self, client):
        response = client.get("/cash_machine")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/cash_machine` не найден. Проверьте настройки в *urls.py*."
        )
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/cash_machine` возвращает ответ со статусом 200."
        )

    def test_qr_code_file_url_exists_at_desired_location(self, client):
        response = client.get("/media/test_file/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/media/test_file/` не найден. Проверьте настройки в *urls.py*."
        )
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/media/test_file/` возвращает ответ со статусом 200."
        )


@pytest.mark.django_db(transaction=True)
class TestAPIURL:
    def test_schema_url_exists_at_desired_location(self, client):
        response = client.get("/api/v1/schema/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/schema/` не найден. Проверьте настройки в " "*urls.py*."
        )
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/schema/` возвращает ответ со статусом 200."
        )

    def test_swagger_url_exists_at_desired_location(self, client):
        response = client.get("/api/v1/swagger-ui/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/swagger-ui/` не найден. Проверьте настройки в " "*urls.py*."
        )
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/swagger-ui/` возвращает ответ со статусом 200."
        )

    def test_redoc_url_exists_at_desired_location(self, client):
        response = client.get("/api/v1/redoc/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/redoc/` не найден. Проверьте настройки в " "*urls.py*."
        )
        assert response.status_code == HTTPStatus.OK, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/redoc/` возвращает ответ со статусом 200."
        )
