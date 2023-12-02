from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema, extend_schema_view, OpenApiParameter,
)

from .serializers import (
    ItemSerializer,
    BadRequestErrorSerializer,
    NotFoundErrorSerializer,
    InternalServerErrorSerializer,
)


check_post_schema = extend_schema_view(
    post=extend_schema(
        request=ItemSerializer(many=True),
        summary="Метод для генерации QR-кода.",
        description="Этот метод позволяет сгенерировать QR-код.",
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
        description="Этот метод позволяет получить чек через QR-код.",
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
