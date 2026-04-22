# Digital Clinic

## Project Overview

This is a **Django** web application designed to provide a seamless interface for CRUD operations on a **PostgreSQL** database. The application focuses on a collaborative environment where data is shared across the organization.

### Key Features

* **Dynamic UI:** Powered by **HTMX** to provide dynamic UI features, such as sortable lists, without full page reloads.
* **Advanced Data Entry:** Includes multi-step forms for complex data workflows.
* **Automated Reporting:** Generates custom PDF reports using **Reportlab**, populating templates with live database data.
* **Secure Access:** Built-in authentication (Login/Logout). To maintain a controlled environment, user registration is handled exclusively via the Django Admin portal.
* **Responsive Design:** Styled with a combination of **Bootstrap** and custom CSS for a modern, mobile-friendly experience.

### Deployment & Architecture

The project is fully containerized and orchestrated using Docker Compose for easy setup and consistency across environments.

The architecture consists of three core services:

* **Web:** The Django application served by **Gunicorn**, a production-grade WSGI Server.
* **Database:** A PostgreSQL instance for persistent data storage.
* **Proxy:** An **Nginx** container serving as a reverse proxy and handling static file delivery.

### Shared Data Model

By design, database entries do not have individual authorship. All authenticated users have access to view and manage the shared dataset, making this ideal for internal team coordination.

## Getting Started

### Environment Variables

Create a `.env` file at the same level as `docker-compose.yml`.

```
# Django
DJANGO_SECRET_KEY= # Random string
DJANGO_ALLOWED_HOSTS= # VPS IP
DJANGO_CSRF_TRUSTED_ORIGINS=https://<vps_ip>:8001 # What to type in the browser's search bar

# Database Settings
DB_ENGINE=postgresql
DB_NAME=db
DB_USERNAME=dc
DB_PASSWORD= # Random string
DB_HOST=db # Docker-compose service name

# Postgres Settings
POSTGRES_DB=db # same as DB_NAME
POSTGRES_USER=dc # same as DB_USERNAME
POSTGRES_PASSWORD= # same as DB_PASSWORD
```

### PDF Generators

For confidentiality reasons, the actual PDF generators were not committed. To create a generator for the `lab` application, copy the template:
```
django_app/apps/core/utils/example_pdf_generator.py
```
to the destination:
```
django_app/apps/lab/utils/lab_pdf_generator.py
```

### Nginx Configuration Files

The application will be deployed using `docker --context`, which builds containers directly on the remote server while the source code files remain on the local machine. However, in order for the Nginx container to be built, the configuration files must be preliminarily uploaded to the server:
```
$ scp -r nginx <user>@<vps_ip>:<absolute_path>/digital-clinic 
```

The specified path must match the one under the `nginx volumes` section in `docker-compose.yml`

### Deployment

The following command starts the application on the remote server. However, in order to run it, one needs an [SSH key](https://www.youtube.com/watch?v=8ugcUTNoGj4):

```
$ docker context create remote-deploy-context --docker "host=ssh://<user>@<vps_ip>"
$ docker --context remote-deploy-context compose up -d --build
```

### Django Administrator

In order to create an account for the administrator, one needs to run the following command on the server:
```
$ docker exec -it <django_container> python manage.py createsuperuser
```
