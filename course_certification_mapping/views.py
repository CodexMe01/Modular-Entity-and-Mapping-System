from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer

class CourseCertificationMappingListCreateAPIView(APIView):
    parent_param = openapi.Parameter('parent_id', openapi.IN_QUERY, description="Filter by parent (Course) ID", type=openapi.TYPE_INTEGER)
    child_param = openapi.Parameter('child_id', openapi.IN_QUERY, description="Filter by child (Certification) ID", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description="List all course certification mappings",
        manual_parameters=[parent_param, child_param],
        responses={200: CourseCertificationMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = CourseCertificationMapping.objects.all()
        parent_id = request.query_params.get('parent_id')
        child_id = request.query_params.get('child_id')

        if parent_id:
            mappings = mappings.filter(parent_id=parent_id)
        if child_id:
            mappings = mappings.filter(child_id=child_id)

        serializer = CourseCertificationMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new course certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve a mapping",
        responses={200: CourseCertificationMappingSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        mapping = get_object_or_404(CourseCertificationMapping, pk=pk)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a mapping (full)",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        mapping = get_object_or_404(CourseCertificationMapping, pk=pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a mapping (partial)",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        mapping = get_object_or_404(CourseCertificationMapping, pk=pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a mapping",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        mapping = get_object_or_404(CourseCertificationMapping, pk=pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
