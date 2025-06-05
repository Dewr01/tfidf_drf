from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document, AnalysisResult
from .serializers import DocumentSerializer, AnalysisResultSerializer
from .utils import calculate_tf, calculate_idf
import chardet


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=False, methods=['post'])
    def analyze(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=400)

        try:
            # Определение кодировки
            raw_content = file.read()
            encoding = chardet.detect(raw_content)['encoding'] or 'utf-8'
            content = raw_content.decode(encoding)

            # Создание документа
            document = Document.objects.create(
                title=request.data.get('title', file.name),
                content=content
            )

            # Анализ TF-IDF
            corpus = self.load_corpus()
            tf = calculate_tf(content)
            idf = calculate_idf(content, corpus)

            # Сохранение результатов
            AnalysisResult.objects.bulk_create([
                AnalysisResult(
                    document=document,
                    word=word,
                    tf=tf_val,
                    idf=idf.get(word, 0)
                ) for word, tf_val in tf.items()
            ])

            # Получение топ-50 результатов
            results = AnalysisResult.objects.filter(document=document).order_by('-idf')[:50]
            serializer = AnalysisResultSerializer(results, many=True)

            return Response({
                'document': DocumentSerializer(document).data,
                'results': serializer.data
            })

        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def load_corpus(self):
        # Здесь должна быть реализация загрузки корпуса
        # Временный пример:
        return [
            "TF-IDF (от англ. TF — term frequency, IDF — inverse document frequency) — статистическая мера,",
            "используемая для оценки важности слова в контексте документа, ",
            "являющегося частью коллекции документов или корпуса."
        ]
