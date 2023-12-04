from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from .serializers import (
    BadRequestErrorSerializer,
    InternalServerErrorSerializer,
    ItemSerializer,
    NotFoundErrorSerializer,
)

check_post_schema = extend_schema_view(
    post=extend_schema(
        request=ItemSerializer(many=True),
        summary="Метод для генерации QR-кода.",
        description="Этот метод позволяет сгенерировать QR-код.\n\n"
        "Используйте камеру смартфона для сканирования QR-кода "
        "из ответа на POST-запрос.\n\n"
        "Пример POST-запроса:\n\n"
        "{\n\n"
        '    "items": [1, 2, 3]\n\n'
        "}",
        responses={
            200: OpenApiResponse(
                description="Документ успешно создан.",
            ),
            400: OpenApiResponse(
                response=BadRequestErrorSerializer,
                description="Error: Bad Request",
            ),
            404: OpenApiResponse(
                response=NotFoundErrorSerializer,
                description="Error: Not Found",
            ),
            500: OpenApiResponse(
                response=InternalServerErrorSerializer,
                description="Error: Internal server error",
            ),
        },
    ),
)


qrcode_get_schema = extend_schema_view(
    get=extend_schema(
        summary="Метод для получения чека через QR-код.",
        description="Этот метод позволяет получить чек через QR-код.\n\n"
        "Открытие файла через Swagger отключено, "
        "потому что он не может отображать PDF-файлы в своём интерфейсе.\n\n"
        "Используйте камеру смартфона для сканирования "
        "QR-кода из ответа на POST-запрос.",
        parameters=[
            OpenApiParameter(
                name="file_name", type=str, location=OpenApiParameter.PATH
            )
        ],
        responses={
            200: OpenApiResponse(
                description="application/pdf",
            ),
            404: OpenApiResponse(
                response=NotFoundErrorSerializer,
                description="Error: Not Found",
            ),
            500: OpenApiResponse(
                response=InternalServerErrorSerializer,
                description="Error: Internal server error",
            ),
        },
    ),
)
