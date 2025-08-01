# TF-IDF DRF API

Простой API для расчета TF-IDF (Term Frequency-Inverse Document Frequency) с использованием Django REST Framework.

## Описание

Этот проект предоставляет REST API для:
1. Загрузки документов (текстовых файлов)
2. Вычисления TF-IDF для загруженных документов
3. Получения списка загруженных документов
4. Получения TF-IDF значений для конкретного документа

## Технологии

- Python 3.x
- Django
- Django REST Framework
- NLTK (для обработки текста)
- SQLite (база данных по умолчанию)

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Dewr01/tfidf_drf.git
   cd tfidf_drf
   ```
   
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```
   
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Примените миграции:
   ```bash
   python manage.py migrate
   ```
   
5. Запустите сервер:
   ```bash
   python manage.py runserver
   ```