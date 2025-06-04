from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class TFIDFResultSerializer(serializers.Serializer):
    word = serializers.CharField()
    tf = serializers.FloatField()
    idf = serializers.FloatField()


class CustomPagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице по умолчанию
    page_size_query_param = 'page_size'  # Параметр для изменения количества элементов на странице
    max_page_size = 100  # Максимальное количество элементов на странице
