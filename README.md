# Проект "Продуктовый помощник"
Адрес проекта: http://51.250.21.194/
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологический стек
![Django-app workflow](https://github.com/kotletka92/foodgram-project-react/actions/workflows/workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)


## Установка
Клонируем репозиторий и переходим в него:
```
git clone <url>
```
Переходим в папку с файлом docker-compose.yaml:
```
cd infra
```
Создаем файл .env в директории infra
```
touch .env
```
Заполнить в настройках репозитория секреты .env
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=615478
DB_HOST=db
DB_PORT=5432
```
Поднимаем контейнеры :
```
docker-compose up -d --build
```
Выполняем миграции:
```
docker-compose exec backend python manage.py migrate
```
Создаем суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
Собираем статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
Создаем дамп (резервную копию) базы:
```
docker-compose exec backend python manage.py dumpdata > fixtures.json
```
> Разместив файл fixtures.json в папке с Dockerfile, можно загрузить в базу данные из дампа:

```
docker-compose exec backend python manage.py loaddata fixtures.json
```
Можно наполнить DB ингредиентами и тэгами:
```
docker-compose exec backend python manage.py load_tags
docker-compose exec backend python manage.py load_ingredients
```
Останавливаем контейнеры:
```
docker-compose stop
```
!Все данные удалятся!
```
docker-compose down -v
```
