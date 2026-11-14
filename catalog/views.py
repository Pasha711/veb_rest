import logging
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Coffee, Origin
from .serializers import CoffeeSerializer, OriginSerializer

logger = logging.getLogger("catalog")


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class OriginListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary="Отримати список регіонів походження",
        responses={200: OriginSerializer(many=True)},
    )
    def get(self, request):
        origins = Origin.objects.all()
        serializer = OriginSerializer(origins, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Створити новий регіон походження (тільки адміністратор)",
        request=OriginSerializer,
        responses={
            201: OriginSerializer,
            400: OpenApiResponse(description="Невалідні вхідні дані"),
            401: OpenApiResponse(description="Необхідна автентифікація"),
            403: OpenApiResponse(description="Доступ дозволено лише адміністраторам"),
        },
    )
    def post(self, request):
        serializer = OriginSerializer(data=request.data)
        if serializer.is_valid():
            origin = serializer.save()
            logger.info("Admin '%s' created Origin id=%s (%s)", request.user.username, origin.id, origin.country)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Validation error while creating Origin: %s", serializer.errors)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OriginDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary="Отримати деталі регіону походження",
        responses={
            200: OriginSerializer,
            404: OpenApiResponse(description="Регіон не знайдено"),
        },
    )
    def get(self, request, pk):
        origin = get_object_or_404(Origin, pk=pk)
        serializer = OriginSerializer(origin)
        return Response(serializer.data)

    @extend_schema(
        summary="Повністю оновити регіон походження (тільки адміністратор)",
        request=OriginSerializer,
        responses={
            200: OriginSerializer,
            400: OpenApiResponse(description="Невалідні дані"),
            403: OpenApiResponse(description="Доступ заборонено"),
            404: OpenApiResponse(description="Регіон не знайдено"),
        },
    )
    def put(self, request, pk):
        origin = get_object_or_404(Origin, pk=pk)
        serializer = OriginSerializer(origin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Admin '%s' updated Origin id=%s", request.user.username, origin.id)
            return Response(serializer.data)
        logger.warning("Validation error while updating Origin id=%s: %s", pk, serializer.errors)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Частково оновити регіон походження (тільки адміністратор)",
        request=OriginSerializer,
        responses={
            200: OriginSerializer,
            400: OpenApiResponse(description="Невалідні дані"),
            403: OpenApiResponse(description="Доступ заборонено"),
            404: OpenApiResponse(description="Регіон не знайдено"),
        },
    )
    def patch(self, request, pk):
        origin = get_object_or_404(Origin, pk=pk)
        serializer = OriginSerializer(origin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Admin '%s' partially updated Origin id=%s", request.user.username, origin.id)
            return Response(serializer.data)
        logger.warning("Validation error while patching Origin id=%s: %s", pk, serializer.errors)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Видалити регіон походження (тільки адміністратор)",
        responses={
            204: OpenApiResponse(description="Успішно видалено"),
            403: OpenApiResponse(description="Доступ заборонено"),
            404: OpenApiResponse(description="Регіон не знайдено"),
            409: OpenApiResponse(description="Конфлікт: регіон використовується в товарах"),
        },
    )
    def delete(self, request, pk):
        origin = get_object_or_404(Origin, pk=pk)
        coffees_count = origin.coffees.count()
        if coffees_count > 0:
            logger.warning("Attempt to delete Origin id=%s with %s linked coffees", pk, coffees_count)
            return Response(
                {
                    "error": f"Неможливо видалити регіон походження, оскільки за ним закріплено {coffees_count} позицій кави."
                },
                status=status.HTTP_409_CONFLICT,
            )

        origin.delete()
        logger.info("Admin '%s' deleted Origin id=%s", request.user.username, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoffeeListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary="Отримати список усіх позицій кави",
        responses={200: CoffeeSerializer(many=True)},
    )
    def get(self, request):
        coffees = Coffee.objects.all()
        serializer = CoffeeSerializer(coffees, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Додати нову позицію кави (тільки адміністратор)",
        request=CoffeeSerializer,
        responses={
            201: CoffeeSerializer,
            400: OpenApiResponse(description="Невалідні вхідні дані"),
            401: OpenApiResponse(description="Необхідна автентифікація"),
            403: OpenApiResponse(description="Доступ дозволено лише адміністраторам"),
        },
    )
    def post(self, request):
        serializer = CoffeeSerializer(data=request.data)
        if serializer.is_valid():
            coffee = serializer.save()
            logger.info("Admin '%s' created Coffee id=%s ('%s')", request.user.username, coffee.id, coffee.title)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Validation error while creating Coffee: %s", serializer.errors)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CoffeeDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary="Отримати детальну інформацію про позицію кави",
        responses={
            200: CoffeeSerializer,
            404: OpenApiResponse(description="Позицію кави не знайдено"),
        },
    )
    def get(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee)
        return Response(serializer.data)

    @extend_schema(
        summary="Повністю оновити позицію кави (тільки адміністратор)",
        request=CoffeeSerializer,
        responses={
            200: CoffeeSerializer,
            400: OpenApiResponse(description="Невалідні дані"),
            401: OpenApiResponse(description="Необхідна автентифікація"),
            403: OpenApiResponse(description="Доступ заборонено"),
            404: OpenApiResponse(description="Позицію кави не знайдено"),
        },
    )
    def put(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Admin '%s' updated Coffee id=%s", request.user.username, coffee.id)
            return Response(serializer.data)
        logger.warning("Validation error while updating Coffee id=%s: %s", pk, serializer.errors)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Частково оновити позицію кави (тільки адміністратор)",
        request=CoffeeSerializer,
        responses={
            200: CoffeeSerializer,
            400: OpenApiResponse(description="Невалідні дані"),
            401: OpenApiResponse(description="Необхідна автентифікація"),
            403: OpenApiResponse(description="Доступ заборонено"),
            404: OpenApiResponse(description="Позицію кави не знайдено"),
        },
    )
    def patch(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Admin '%s' partially updated Coffee id=%s", request.user.username, coffee.id)
            return Response(serializer.data)
        logger.warning("Validation error while patching Coffee id=%s: %s", pk, serializer.errors)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Видалити позицію кави (тільки адміністратор)",
        responses={
            204: OpenApiResponse(description="Позицію кави видалено"),
            401: OpenApiResponse(description="Необхідна автентифікація"),
            403: OpenApiResponse(description="Доступ заборонено"),
            404: OpenApiResponse(description="Позицію кави не знайдено"),
        },
    )
    def delete(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        coffee.delete()
        logger.info("Admin '%s' deleted Coffee id=%s", request.user.username, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)