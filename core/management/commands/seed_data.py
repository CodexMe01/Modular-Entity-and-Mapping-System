from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certifications.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping

class Command(BaseCommand):
    help = 'Seeds the database with initial dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Vendors
        v1, _ = Vendor.objects.get_or_create(code='V001', defaults={'name': 'Vendor One', 'description': 'First vendor'})
        v2, _ = Vendor.objects.get_or_create(code='V002', defaults={'name': 'Vendor Two', 'description': 'Second vendor'})

        # Products
        p1, _ = Product.objects.get_or_create(code='P001', defaults={'name': 'Product One', 'description': 'First product'})
        p2, _ = Product.objects.get_or_create(code='P002', defaults={'name': 'Product Two', 'description': 'Second product'})
        p3, _ = Product.objects.get_or_create(code='P003', defaults={'name': 'Product Three', 'description': 'Third product'})

        # Courses
        c1, _ = Course.objects.get_or_create(code='C001', defaults={'name': 'Course One', 'description': 'First course'})
        c2, _ = Course.objects.get_or_create(code='C002', defaults={'name': 'Course Two', 'description': 'Second course'})

        # Certifications
        cert1, _ = Certification.objects.get_or_create(code='CERT001', defaults={'name': 'Cert One', 'description': 'First cert'})
        cert2, _ = Certification.objects.get_or_create(code='CERT002', defaults={'name': 'Cert Two', 'description': 'Second cert'})

        # Mappings
        # Vendor -> Product
        VendorProductMapping.objects.get_or_create(parent=v1, child=p1, defaults={'primary_mapping': True})
        VendorProductMapping.objects.get_or_create(parent=v1, child=p2, defaults={'primary_mapping': False})
        VendorProductMapping.objects.get_or_create(parent=v2, child=p3, defaults={'primary_mapping': True})

        # Product -> Course
        ProductCourseMapping.objects.get_or_create(parent=p1, child=c1, defaults={'primary_mapping': True})
        ProductCourseMapping.objects.get_or_create(parent=p1, child=c2, defaults={'primary_mapping': False})
        ProductCourseMapping.objects.get_or_create(parent=p2, child=c2, defaults={'primary_mapping': True})

        # Course -> Certification
        CourseCertificationMapping.objects.get_or_create(parent=c1, child=cert1, defaults={'primary_mapping': True})
        CourseCertificationMapping.objects.get_or_create(parent=c1, child=cert2, defaults={'primary_mapping': False})

        self.stdout.write(self.style.SUCCESS("Successfully seeded data!"))
