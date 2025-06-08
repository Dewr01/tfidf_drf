import os
from typing import List, TextIO
from django.conf import settings
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()


class CorpusLoader:
    """Класс для загрузки и управления корпусом документов"""

    # Конфигурация из переменных окружения
    CORPUS_CACHE_KEY: str = os.getenv('CORPUS_CACHE_KEY', 'tfidf_corpus')
    CORPUS_TTL: int = int(os.getenv('CORPUS_CACHE_TTL', 60 * 60 * 24))  # 24 часа по умолчанию
    CORPUS_FILE_PATH: str = os.getenv(
        'CORPUS_FILE_PATH',
        os.path.join(settings.BASE_DIR, 'data', 'corpus.txt')
    )

    @classmethod
    def load_corpus(cls) -> List[str]:
        """
        Основной метод для загрузки корпуса с кэшированием
        Возвращает:
            List[str]: Список документов корпуса. Если корпус есть в кэше - возвращает из кэша,
                  иначе загружает из файла, кэширует и возвращает.

        Пример:
            corpus = CorpusLoader.load_corpus()
            len(corpus) > 0
            True
        """
        corpus: List[str] = cache.get(cls.CORPUS_CACHE_KEY)
        if corpus is None:
            corpus = cls._load_from_file()
            cache.set(cls.CORPUS_CACHE_KEY, corpus, cls.CORPUS_TTL)
        return corpus

    @classmethod
    def _load_from_file(cls) -> List[str]:
        """
        Загружает корпус из файла, указанного в CORPUS_FILE_PATH
        Возвращает:
            List[str]: Список документов, загруженных из файла.
                  Если файл не найден, возвращает корпус по умолчанию.
        Исключения:
            ValueError: Если произошла ошибка при чтении файла
        """
        try:
            os.makedirs(os.path.dirname(cls.CORPUS_FILE_PATH), exist_ok=True)

            with open(cls.CORPUS_FILE_PATH, 'r', encoding='utf-8') as f:
                return cls._process_file_content(f)
        except FileNotFoundError:
            return cls._get_default_corpus()
        except Exception as e:
            raise ValueError(f"Ошибка загрузки корпуса: {str(e)}")

    @staticmethod
    def _process_file_content(file_handler: TextIO) -> List[str]:
        """
        Обрабатывает содержимое файла корпуса

        Аргументы:
            file_handler (TextIO): Файловый объект, открытый для чтения
        Возвращает:
            List[str]: Список документов, извлеченных из файла.
                   Пустые строки используются как разделители документов.
        """
        documents: List[str] = []
        current_doc: List[str] = []

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
    def _get_default_corpus() -> List[str]:
        """
        Возвращает корпус по умолчанию
        Возвращает:
            List[str]: Стандартный корпус документов о TF-IDF.
                Используется когда основной файл корпуса недоступен.
        """
        return [
            "TF-IDF (от англ. term frequency - inverse document frequency) - статистическая мера",
            "Используется для оценки важности слова в документе, являющемся частью коллекции",
            "Чем чаще слово встречается в документе и реже в коллекции, тем выше его вес"
        ]

    @classmethod
    def clear_cache(cls) -> None:
        """
        Очищает кэшированную версию корпуса
        После вызова этого метода следующий вызов load_corpus()
        будет загружать корпус заново."""
        cache.delete(cls.CORPUS_CACHE_KEY)
