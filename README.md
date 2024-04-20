# HW_web_14

REST_API:

Для роботи проекта необхідний файл `.env` зі змінними оточення.
Створіть його згідно прикладу у файлі .env.example та підставте свої значення.

Запуск баз даних

```bash
docker-compose up -d
```

Запуск застосунку

```
py main.py
```

ДОКУМЕНТАЦІЯ:

ПОСИЛАННЯ НА СТОРІНКУ З ДОКУМЕНТАЦІЄЮ ЗНАХОДИТЬСЯ В ДИРЕКТОРІЇ docs/build/html/index.html

ТЕСТИ:

Запуск фреймворку pytest для перевірки тестів у директорії tests:

```
pytest -v tests/
```

Запуск пакету pytest-cov для контролю тестів:

```
pytest -v --cov=./src --cov-report html tests/
```

Coverage HTML written to dir htmlcov
