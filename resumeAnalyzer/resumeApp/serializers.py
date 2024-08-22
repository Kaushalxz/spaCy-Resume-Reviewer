from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('id', 'file', 'uploaded_at', 'text_content', 'analysis_results')
        read_only_fields = ('uploaded_at', 'text_content', 'analysis_results')

    def create(self, validated_data):
        # Create the Resume instance first
        resume = Resume.objects.create(**validated_data)
        return resume
