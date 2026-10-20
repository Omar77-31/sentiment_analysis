import re
from rest_framework import serializers
from .models import AnalysisResult


class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = ["id", "text", "sentiment", "confidence", "latency_ms", "memory_mb", "created_at"]


class AnalyzeRequestSerializer(serializers.Serializer):
    text = serializers.CharField(
        max_length=2000,
        trim_whitespace=True,
        error_messages={
            "blank": "Text cannot be empty.",
            "max_length": "Text is too long (maximum 2000 characters)."
        }
    )

    def validate_text(self, value):
        if not re.search(r'[\u0600-\u06FF]', value):
            raise serializers.ValidationError("Text must contain Arabic characters.")
        return value