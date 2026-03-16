from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer

class VendorProductMappingListCreateAPIView(APIView):
    parent_param = openapi.Parameter('parent_id', openapi.IN_QUERY, description="Filter by parent (Vendor) ID", type=openapi.TYPE_INTEGER)
    child_param = openapi.Parameter('child_id', openapi.IN_QUERY, description="Filter by child (Product) ID", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description="List all vendor product mappings",
        manual_parameters=[parent_param, child_param],
        responses={200: VendorProductMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = VendorProductMapping.objects.all()
        parent_id = request.query_params.get('parent_id')
        child_id = request.query_params.get('child_id')

        if parent_id:
            mappings = mappings.filter(parent_id=parent_id)
        if child_id:
            mappings = mappings.filter(child_id=child_id)

        serializer = VendorProductMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new vendor product mapping",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve a mapping",
        responses={200: VendorProductMappingSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        mapping = get_object_or_404(VendorProductMapping, pk=pk)
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a mapping (full)",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        mapping = get_object_or_404(VendorProductMapping, pk=pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a mapping (partial)",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        mapping = get_object_or_404(VendorProductMapping, pk=pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a mapping",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        mapping = get_object_or_404(VendorProductMapping, pk=pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
