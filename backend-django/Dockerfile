FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
# Dummy DATABASE_URL para collectstatic durante build
ARG DATABASE_URL=postgresql://postgres:dummy@localhost/dummy
ARG DJANGO_SECRET_KEY=dummy-secret-key-for-build
RUN DATABASE_URL=$DATABASE_URL DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY python manage.py collectstatic --noinput --clear
EXPOSE 8000
CMD ["gunicorn", "orion_api.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
