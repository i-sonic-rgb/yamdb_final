ReadMe
# Проект YaMDB Final
![event parameter](https://github.com/i-sonic-rgb/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

https://github.com/i-sonic-rgb/yamdb_final

## Общее описание
Проект сайта для выставления оценок (рейтинга) и комментариев для произведений.
На сайте администратором загружаются наименования произведений, которые относятся к различным категориям (книги, музыка, фильмы) и жанрам (комедия, хоррор) 
Зарегистрированные пользователи могут ставить оценки произведениям (от 1 до 10), писать рецензии (не более 1 рецензии от 1 пользователя на произведение).
Также зарегистрированные пользователи могут оставлять комментарии к рецензиям.

Проект доступен по адресу: sonicyap.myftp.org или IP: 158.160.12.170 UPD - в связи с новым учебным проектом по данному адресу проект более недоступен  

### Технологии
- Python 
- Django 
- DjangoRest Framework
- Nginx
- Gunicorn
- Docker, Docker compose
- GitHub Workflow

## Инструкция по запуску на локальном компьютере
### Шаблон .env файла
В папке /yamdb_final/infra/, создать файл .env со седующими переменными (формат НАЗВАНИЕ_ПЕРЕМЕННОЙ=ТЕКСТ, например DB_ENGINE=django.db.backends.postgresql): 
- DB_ENGINE - указывается вид БД (по умолчанию - 'django.db.backends.postgresql')
- DB_NAME - имя базы данных (по умолчанию - 'postgres')
- POSTGRES_USER - логин для подключения к базе данных (по умолчанию - 'postgres')
- POSTGRES_PASSWORD - пароль для подключения к БД (установите свой)
- DB_HOST - название сервиса БД (контейнера; по умолчанию 'db')
- DB_PORT - порт доступа к БД (по умолчанию - 5432)
- DJANGO_SECRET_KEY - секретный код для доступа к Джанго (settings.py SECRET_KEY)

### Запуск docker контейнеров
- клонируйте проект в рабочую папку: sudo git clone ...
- установите docker и docker-compose: https://docs.docker.com/compose/install/
- в терминале откройте папку /yamdb_final/infra/
- запустите контейнеры: sudo docker-compose up
- если после запуска потребуется обновить код - внесите правки и в терминале наберите sudo docker-compose up -d --build
- наберите sudo docker-compose exec web python manage.py makemigrations reviews
- наберите sudo docker-compose exec web python manage.py migrate
- наберите sudo docker-compose exec web python manage.py createsuperuser
- наберите sudo docker-compose exec web python manage.py collectstatic --no-input
- чтобы удалить контейнеры и зависимости: sudo docker-compose down -v

## Инструкция по запуску на сервере
- На сервере должны быть установлены Docker, docker-compose
- Требуется получение сертифика SSL для работы домена
### Инструкции при первом запуске на сервере
- загрузите на сервер в рабочую папку файл docker-compose.yaml и скрипт из статьи https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71 
- загрузите на сервер в папку ~/nginx/ файл default.config
Запустите скрипт за запуска сервера с SSL:
- sudo ./init-letsencrypt.sh
Запустите миграции:
- sudo docker-compose exec web python manage.py collectstatic
- sudo docker-compose exec web python manage.py makemigrations reviews
- sudo docker-compose exec web python manage.py migrate

## Доступные эндпоинты
- sonicyap.myftp.org/redoc/ - файл redoc
- sonicyap.myftp.org/admin/ - панель администирования
- sonicyap.myftp.org/api/v1/ - api сайта

## Авторы
### Бэкенд:
- Igor Poliakov
- Nikita Freyuk
- Andrey Rodin
### Инфраструктура, workflow и развертывание на сервере:
- Igor Poliakov
