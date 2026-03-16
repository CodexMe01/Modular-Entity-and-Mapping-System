from rest_framework import serializers
from .models import ProductCourseMapping

class ProductCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCourseMapping
        fields = ['id', 'parent', 'child', 'primary_mapping', 'is_active', 'created_at', 'updated_at']

    def validate(self, data):
        parent = data.get('parent')
        child = data.get('child')
        primary_mapping = data.get('primary_mapping', False)

        if primary_mapping:
            # Check if another primary mapping exists for this parent
            qs = ProductCourseMapping.objects.filter(parent=parent, primary_mapping=True)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"primary_mapping": "Only one primary mapping is allowed per parent at a time."})

        return data
