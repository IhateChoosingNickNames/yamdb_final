# YamDb

Description: API for YamDb

Used technologies:
-
    - python 3.9
    - django 2.2.16
    - djangorestframework 3.12.4
    - simplejwt 4.7.2
    - django-filters 21.1
    - Postgresql
    - dotenv 0.21.1
    - Docker 20.10.22
Features:
-
    - Authorization via email adress
    - Diffrent roles for users: common user, modertor, admin
    - Manage users and content
    - Cusomize your profile
    - Create reviews for titles
    - Rate titles
    - Comment reviews

Instructions:

## enviroment:
Create .env file infra/.env and fill it with required keys:
- SECRET_KEY=...
- DB_ENGINE=...
- DB_NAME=...
- POSTGRES_USER=...
- POSTGRES_PASSWORD=...
- DB_HOST=db
- DB_PORT=5432

## Local launch:

1. Install requirements:
    #### pip install -r requirements.txt
2. Go to ../api_yamdb/ migrate:
    #### python manage.py migrate
3. Fill the DB with prepared CSV-files:
    #### python manage.py fill_db
4. Runserver:
    #### python manage.py runserver
After that site is available at your localhost url (most common case: http://127.0.0.1:8000/)

## Docker:
1. Build containers:
    #### docker-compose up -d --build
2. Migrate DB:
    #### docker-compose exec web python manage.py migrate
3. Collect static:
    #### winpty docker-compose exec web python manage.py collectstatic --no-input
For now app is available at localhost

### Some additional commands: 
4. Fill DB with some test data:
    #### docker-compose exec web python manage.py fill_db
5. Create admin:
    #### winpty docker-compose exec web python manage.py createsuperuser
6. To make dump of DB:
    #### docker-compose exec web python manage.py dumpdata > your_fixture_name.json
7. To load fixtures:
    #### docker-compose exec web python manage.py loaddata your_fixture_name.json

If you'll need any *manage.py* commands then you'll want to use prefix:

    docker-compose exec web python manage.py *comand*

Examples of endpoints:
-
    - GET http://your_ip:your_port/api/v1/titles/{title_id}/
    - POST http://your_ip:your_port/api/v1/titles/
    - DELETE http://your_ip:your_port/api/v1/posts/1/
    - PUT http://your_ip:your_port/api/v1/posts/1/

Examples of responses:
-
- GET title:
~~~
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{
"name": "string",
"slug": "string"
}
],
"category": {
"name": "string",
"slug": "string"
}
}
~~~
- POST title:
~~~
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
~~~
All available endpoints and responses you can find in documentation:

    # http://your_ip:your_port/redoc

[![YaMDb workflow](https://github.com/IhateChoosingNickNames/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/IhateChoosingNickNames/yamdb_final/actions/workflows/yamdb_workflow.yml)
