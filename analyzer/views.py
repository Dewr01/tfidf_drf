from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import render
from .logic import calculate_tf, calculate_idf

DEFAULT_TEXT = [
    "TF-IDF (от англ. TF — term frequency, IDF — inverse document frequency) — статистическая мера,",
    "используемая для оценки важности слова в контексте документа, ",
    "являющегося частью коллекции документов или корпуса."
]


class TFIDFAnalyzerView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'analyzer/upload_form.html'

    def get(self, request):
        """Отображает форму загрузки файла"""
        return render(request, self.template_name, {'title': 'TF-IDF Analyzer'})

    def post(self, request):
        """Обрабатывает загруженный файл и возвращает результаты"""
        if 'file' not in request.FILES:
            return render(
                request,
                self.template_name,
                {'error': 'Файл не загружен', 'title': 'Ошибка'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            file = request.FILES['file']

            # Проверка типа файла
            if not file.name.endswith('.txt'):
                raise ValueError("Поддерживаются только .txt файлы")

            # Чтение и обработка файла
            text = file.read().decode('utf-8')

            # Вычисление TF и IDF
            tf = calculate_tf(text)
            idf = calculate_idf(text, DEFAULT_TEXT)

            # Формирование результатов
            results = [
                {"word": word, "tf": tf[word], "idf": idf.get(word, 0)}
                for word in tf
            ]

            # Сортировка и выбор топ-50
            results.sort(key=lambda x: x["idf"], reverse=True)
            top_50 = results[:50]

            return render(
                request,
                self.template_name,
                {
                    'title': 'Результаты анализа',
                    'results': top_50,
                    'filename': file.name,
                    'success': True
                }
            )

        except UnicodeDecodeError:
            error = "Ошибка декодирования файла. Убедитесь, что файл в кодировке UTF-8"
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Произошла ошибка: {str(e)}"

        return render(
            request,
            self.template_name,
            {'error': error, 'title': 'Ошибка'},
            status=status.HTTP_400_BAD_REQUEST
        )
