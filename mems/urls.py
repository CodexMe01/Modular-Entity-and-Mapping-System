from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MEMS API",
        default_version='v1',
        description="Modular Entity and Mapping System API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/vendors/', include('vendor.urls')),
    path('api/products/', include('product.urls')),
    path('api/courses/', include('course.urls')),
    path('api/certifications/', include('certifications.urls')),
    path('api/vendor-product-mappings/', include('vendor_product_mapping.urls')),
    path('api/product-course-mappings/', include('product_course_mapping.urls')),
    path('api/course-certification-mappings/', include('course_certification_mapping.urls')),
]
