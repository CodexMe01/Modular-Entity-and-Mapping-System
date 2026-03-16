from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer

class ProductCourseMappingListCreateAPIView(APIView):
    parent_param = openapi.Parameter('parent_id', openapi.IN_QUERY, description="Filter by parent (Product) ID", type=openapi.TYPE_INTEGER)
    child_param = openapi.Parameter('child_id', openapi.IN_QUERY, description="Filter by child (Course) ID", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description="List all product course mappings",
        manual_parameters=[parent_param, child_param],
        responses={200: ProductCourseMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = ProductCourseMapping.objects.all()
        parent_id = request.query_params.get('parent_id')
        child_id = request.query_params.get('child_id')

        if parent_id:
            mappings = mappings.filter(parent_id=parent_id)
        if child_id:
            mappings = mappings.filter(child_id=child_id)

        serializer = ProductCourseMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new product course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve a mapping",
        responses={200: ProductCourseMappingSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        mapping = get_object_or_404(ProductCourseMapping, pk=pk)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a mapping (full)",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        mapping = get_object_or_404(ProductCourseMapping, pk=pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a mapping (partial)",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        mapping = get_object_or_404(ProductCourseMapping, pk=pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a mapping",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        mapping = get_object_or_404(ProductCourseMapping, pk=pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
