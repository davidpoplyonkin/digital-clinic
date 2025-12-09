ARG DJANGO_ALLOWED_HOSTS
ARG DJANGO_CSRF_TRUSTED_ORIGINS
ARG DJANGO_SETTINGS_MODULE
ARG DB_ENGINE

FROM python:3.13-slim


ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS
ENV DJANGO_CSRF_TRUSTED_ORIGINS=$DJANGO_CSRF_TRUSTED_ORIGINS
ENV DB_ENGINE=$DB_ENGINE
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# for psycopg
RUN apt-get update && apt-get install -y libpq-dev

# for formtools
RUN pip install --no-cache-dir --upgrade setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN chmod +x ./start.sh
CMD ["./start.sh"]