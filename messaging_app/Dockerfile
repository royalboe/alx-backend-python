FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

LABEL author="Ayomide Johnson Salami" \
      email="auomidejohnson@gmail.com"

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]