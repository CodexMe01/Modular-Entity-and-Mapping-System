from django.db import models
from django.core.exceptions import ValidationError
from core.models import TimeStampedModel
from vendor.models import Vendor
from product.models import Product

class VendorProductMapping(TimeStampedModel):
    parent = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='product_mappings')
    child = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendor_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ('parent', 'child')

    def clean(self):
        super().clean()
        if self.primary_mapping:
            existing_primary = VendorProductMapping.objects.filter(parent=self.parent, primary_mapping=True).exclude(pk=self.pk).exists()
            if existing_primary:
                raise ValidationError({"primary_mapping": "Only one primary mapping is allowed per parent."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.name} -> {self.child.name}"
