from django.urls import path
from .views import TFIDFAnalyzerView

urlpatterns = [
    path('analyze/', TFIDFAnalyzerView.as_view(), name='tfidf-analyzer'),
]
