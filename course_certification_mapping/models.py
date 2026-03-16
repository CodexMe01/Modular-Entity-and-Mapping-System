from django.db import models
from django.core.exceptions import ValidationError
from core.models import TimeStampedModel
from course.models import Course
from certifications.models import Certification

class CourseCertificationMapping(TimeStampedModel):
    parent = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certification_mappings')
    child = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='course_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ('parent', 'child')

    def clean(self):
        super().clean()
        if self.primary_mapping:
            existing_primary = CourseCertificationMapping.objects.filter(parent=self.parent, primary_mapping=True).exclude(pk=self.pk).exists()
            if existing_primary:
                raise ValidationError({"primary_mapping": "Only one primary mapping is allowed per parent."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.name} -> {self.child.name}"
