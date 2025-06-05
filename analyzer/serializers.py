from rest_framework import serializers
from .models import Document, AnalysisResult


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'uploaded_at']


class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = ['word', 'tf', 'idf']


class TFIDFAnalysisSerializer(serializers.Serializer):
    document = DocumentSerializer()
    results = AnalysisResultSerializer(many=True)
