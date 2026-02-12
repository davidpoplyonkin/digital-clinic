ARG DJANGO_ALLOWED_HOSTS
ARG DJANGO_CSRF_TRUSTED_ORIGINS
ARG DJANGO_SETTINGS_MODULE
ARG DB_ENGINE

# --- STAGE 1: Build CSS ---
FROM node:20-slim AS build-assets
WORKDIR /usr/src/app

# Install the sass compiler
RUN npm install -g sass
RUN npm install bootstrap@5.3.0

# Copy only the files needed for CSS compilation
COPY ./static/scss/base.scss .

# Compile
RUN sass base.scss base.css --style compressed --load-path=node_modules

# --- STAGE 2: Final Django Image ---
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

# Copy the compiled CSS from the first stage
COPY --from=build-assets /usr/src/app/base.css ./static/css/base.css

RUN chmod +x ./start.sh
CMD ["./start.sh"]