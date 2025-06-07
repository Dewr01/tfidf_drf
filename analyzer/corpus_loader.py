import os
from django.conf import settings
from django.core.cache import cache


class CorpusLoader:
    """Класс для загрузки и управления корпусом документов"""

    CORPUS_CACHE_KEY = 'tfidf_corpus'
    CORPUS_TTL = 60 * 60 * 24  # 24 часа кэширования

    @classmethod
    def load_corpus(cls):
        """Основной метод для загрузки корпуса с кэшированием"""
        corpus = cache.get(cls.CORPUS_CACHE_KEY)
        if corpus is None:
            corpus = cls._load_from_file()
            cache.set(cls.CORPUS_CACHE_KEY, corpus, cls.CORPUS_TTL)
        return corpus

    @classmethod
    def _load_from_file(cls):
        """Загружает корпус из файла"""
        corpus_path = os.path.join(settings.BASE_DIR, 'corpus.txt')

        try:
            with open(corpus_path, 'r', encoding='utf-8') as f:
                return cls._process_file_content(f)
        except FileNotFoundError:
            return cls._get_default_corpus()
        except Exception as e:
            raise ValueError(f"Ошибка загрузки корпуса: {str(e)}")

    @staticmethod
    def _process_file_content(file_handler):
        """Обрабатывает содержимое файла корпуса"""
        documents = []
        current_doc = []

        for line in file_handler:
            line = line.strip()
            if line:
                current_doc.append(line)
            elif current_doc:
                documents.append(' '.join(current_doc))
                current_doc = []

        if current_doc:
            documents.append(' '.join(current_doc))

        return documents or CorpusLoader._get_default_corpus()

    @staticmethod
    def _get_default_corpus():
        """Возвращает корпус по умолчанию"""
        return [
            "TF-IDF (от англ. term frequency - inverse document frequency) - статистическая мера",
            "Используется для оценки важности слова в документе, являющемся частью коллекции",
            "Чем чаще слово встречается в документе и реже в коллекции, тем выше его вес"
        ]

    @classmethod
    def clear_cache(cls):
        """Очищает кэш корпуса"""
        cache.delete(cls.CORPUS_CACHE_KEY)
