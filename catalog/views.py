from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Origin, Coffee
from .serializers import OriginSerializer, CoffeeSerializer


class OriginListCreateView(APIView):
    def get(self, request):
        origins = Origin.objects.all()
        serializer = OriginSerializer(origins, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OriginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OriginDetailView(APIView):
    def get(self, request, pk):
        origin = get_object_or_404(Origin, pk=pk)
        serializer = OriginSerializer(origin)
        return Response(serializer.data)

    def put(self, request, pk):
        origin = get_object_or_404(Origin, pk=pk)
        serializer = OriginSerializer(origin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        origin = get_object_or_404(Origin, pk=pk)
        coffees_count = origin.coffees.count()
        if coffees_count > 0:
            return Response(
                {
                    "error": f"Неможливо видалити регіон походження, оскільки за ним закріплено {coffees_count} позицій кави."
                },
                status=status.HTTP_409_CONFLICT
            )

        origin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoffeeListCreateView(APIView):
    def get(self, request):
        coffees = Coffee.objects.all()
        serializer = CoffeeSerializer(coffees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CoffeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CoffeeDetailView(APIView):
    def get(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee)
        return Response(serializer.data)

    def put(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"error": "Невалідні дані", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        coffee = get_object_or_404(Coffee, pk=pk)
        coffee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
