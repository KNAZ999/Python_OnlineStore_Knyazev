# Используем официальный образ Python 3.12
FROM python:3.12-slim-bullseye

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /site_Knyazev

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /site_Knyazev

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска приложения (используем runserver для разработки)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]