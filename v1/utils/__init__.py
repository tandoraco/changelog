from rest_framework import status
from rest_framework.response import Response


def serializer_error_response(serializer):
    return Response(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        data=serializer.errors)


def unprocessable_entity(detail):
    return Response(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        data={
            'detail': detail
        }
    )
