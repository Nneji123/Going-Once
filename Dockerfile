FROM python:3.8.13-slim-bullseye

WORKDIR /app

RUN pip install --upgrade setuptools

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

# Create migrations directory and __init__.py files
RUN mkdir -p core/migrations && touch core/migrations/__init__.py
RUN mkdir -p customauth/migrations && touch customauth/migrations/__init__.py

EXPOSE 8000

# Run migrations and create superuser using email and password from .env file
RUN python manage.py makemigrations
RUN python manage.py migrate --run-syncdb

RUN python manage.py customcreatesuperuser

RUN python manage.py collectstatic --no-post-process --no-input --upload-unhashed-files

CMD celery -A backend beat -l info --detach && \
    celery -A backend worker -l info --detach && \
    gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --env DJANGO_CONFIGURATION=ProdConfig
