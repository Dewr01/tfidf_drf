from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .corpus_loader import CorpusLoader
from .models import Document, AnalysisResult
from .serializers import DocumentSerializer, AnalysisResultSerializer
from .utils import calculate_tf, calculate_idf
import chardet


class MainView(TemplateView):
    """Главная страница приложения"""
    template_name = 'analyzer/main.html'


def _validate_file(request):
    """Проверка наличия и валидация файла"""
    if 'file' not in request.FILES:
        raise ValueError("Файл не был предоставлен")

    file = request.FILES['file']
    if not file.name.lower().endswith('.txt'):
        raise ValueError("Поддерживаются только файлы .txt")

    return file


def _create_document(request, file, content):
    """Создание документа в базе данных"""
    return Document.objects.create(
        title=request.data.get('title', file.name),
        content=content
    )


def _read_file_content(file):
    """Чтение и декодирование содержимого файла"""
    raw_content = file.read()
    encoding = chardet.detect(raw_content)['encoding'] or 'utf-8'

    try:
        return raw_content.decode(encoding)
    except UnicodeDecodeError:
        raise ValueError("Не удалось декодировать файл. Проверьте кодировку.")


def _prepare_response(document, results):
    """Подготовка ответа API"""
    return Response({
        'document': DocumentSerializer(document).data,
        'results': AnalysisResultSerializer(results, many=True).data
    })





def _perform_tfidf_analysis(document, content):
    """Выполнение TF-IDF анализа и сохранение результатов"""
    corpus = _load_corpus()
    tf = calculate_tf(content)
    idf = calculate_idf(content, corpus)

    # Создание записей AnalysisResult
    analysis_results = [
        AnalysisResult(
            document=document,
            word=word,
            tf=tf_val,
            idf=idf.get(word, 0)
        ) for word, tf_val in tf.items()
    ]

    # Массовое создание записей
    AnalysisResult.objects.bulk_create(analysis_results)

    return AnalysisResult.objects.filter(document=document).order_by('-idf')[:50]


def _load_corpus():
    """Загружает корпус документов (пока просто вызывает CorpusLoader)"""
    return CorpusLoader.load_corpus()


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=False, methods=['post'])
    def analyze(self, request):
        """Основной метод обработки анализа документа"""
        try:
            # Валидация и загрузка файла
            file = _validate_file(request)

            # Чтение и декодирование содержимого
            content = _read_file_content(file)

            # Создание документа
            document = _create_document(request, file, content)

            # Анализ TF-IDF
            results = _perform_tfidf_analysis(document, content)

            # Возврат результатов
            return _prepare_response(document, results)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
