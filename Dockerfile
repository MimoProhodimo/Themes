FROM python:3.11-slim

WORKDIR /app

# Копируем requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем папки для файлов
RUN mkdir -p uploads themes

# Запускаем бота
CMD ["python", "bot.py"]