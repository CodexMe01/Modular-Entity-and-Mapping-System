from rest_framework import serializers
from .models import VendorProductMapping

class VendorProductMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProductMapping
        fields = ['id', 'parent', 'child', 'primary_mapping', 'is_active', 'created_at', 'updated_at']

    def validate(self, data):
        parent = data.get('parent')
        child = data.get('child')
        primary_mapping = data.get('primary_mapping', False)

        # Skip unique together validation if it's already handled by DRF's default validators
        # but DRF handles model unique_together automatically if fields are present.

        if primary_mapping:
            # Check if another primary mapping exists for this parent
            qs = VendorProductMapping.objects.filter(parent=parent, primary_mapping=True)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"primary_mapping": "Only one primary mapping is allowed per parent at a time."})

        return data
