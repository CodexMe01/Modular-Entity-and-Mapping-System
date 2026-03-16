from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from .models import Certification
from .serializers import CertificationSerializer

class CertificationListCreateAPIView(APIView):
    name_param = openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING)
    is_active_param = openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(
        operation_description="List all certifications",
        manual_parameters=[name_param, is_active_param],
        responses={200: CertificationSerializer(many=True)}
    )
    def get(self, request):
        certifications = Certification.objects.all()
        name = request.query_params.get('name')
        is_active = request.query_params.get('is_active')

        if name:
            certifications = certifications.filter(name__icontains=name)
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            certifications = certifications.filter(is_active=is_active_bool)

        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new certification",
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve a certification",
        responses={200: CertificationSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        certification = get_object_or_404(Certification, pk=pk)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a certification (full)",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        certification = get_object_or_404(Certification, pk=pk)
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a certification (partial)",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        certification = get_object_or_404(Certification, pk=pk)
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a certification",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        certification = get_object_or_404(Certification, pk=pk)
        certification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
