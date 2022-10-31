ReadMe
# YaMDB
![example event parameter](https://github.com/i-sonic-rgb/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)
## Общее описание
Проект сайта для выставления оценок (рейтинга) и комментариев для произведений.
На сайте администратором загружаются наименования произведений, которые относятся к различным категориям (книги, музыка, фильмы) и жанрам (комедия, хоррор) 
Зарегистрированные пользователи могут ставить оценки произведениям (от 1 до 10), писать рецензии (не более 1 рецензии от 1 пользователя на произведение).
Также зарегистрированные пользователи могут оставлять комментарии к рецензиям.

### Технологии
- Python 
- Django 
- DjangoRest Framework
- Nginx
- Gunicorn
- Docker, Docker compose
- GitHub Workflow

## Инструкция по заапуску
### Шаблон .env файла
В папке /infra_sp2/infra/, создать файл .env со седующими переменными (формат НАЗВАНИЕ_ПЕРЕМЕННОЙ=ТЕКСТ, например DB_ENGINE=django.db.backends.postgresql): 
- DB_ENGINE - указывается вид БД (по умолчанию - 'django.db.backends.postgresql')
- DB_NAME - имя базы данных (по умолчанию - 'postgres')
- POSTGRES_USER - логин для подключения к базе данных (по умолчанию - 'postgres')
- POSTGRES_PASSWORD - пароль для подключения к БД (установите свой)
- DB_HOST - название сервиса БД (контейнера; по умолчанию 'db')
- DB_PORT - порт доступа к БД (по умолчанию - 5432)
- DJANGO_SECRET_KEY - секретный код для доступа к Джанго (settings.py SECRET_KEY)

### Запуск docker контейнеров
- клонируйте проект в рабочую папку: sudo git clone git@github.com:i-sonic-rgb/infra_sp2.git
- установите docker и docker-compose: https://docs.docker.com/compose/install/
- в терминале откройте папку /infra_sp2/infra/
- запустите контейнеры: sudo docker-compose up
- если после запуска потребуется обновить код - внесите правки и в терминале наберите sudo docker-compose up -d --build
- наберите sudo docker-compose exec web python manage.py makemigrations reviews
- наберите sudo docker-compose exec web python manage.py migrate
- наберите sudo docker-compose exec web python manage.py createsuperuser
- наберите sudo docker-compose exec web python manage.py collectstatic --no-input
- для загрузки данных в базу данных из файла fixtures.json наберите: sudo docker-compose exec web python manage.py loaddata fixtures.json
- чтобы удалить контейнеры и зависимости: sudo docker-compose down -v

### Доступные эндпоинты
- localhost/redoc/ - файл redoc
- localhost/admin/ - панель администирования
- localhost/api/v1/ - api сайта

## Авторы
### Бэкенд:
- Igor Poliakov
- Nikita Freyuk
- Andrey Rodin
### Инфраструктура, workflow и развертывание на сервере:
- Igor Poliakov