
**сайт доступен http://51.250.0.169/
админка root@roor.ru пароль root**

## Проект Foodgram

*Foodgram реализован для публикации рецептов. Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачать список покупок ингредиентов для добавленных в покупки рецептов.*

Подготовка и запуск проекта

Склонировать репозиторий на локальную машину: 

    git clone git@github.com:Antisyslik/foodgram-project-react.git 

Для работы с удаленным сервером (на ubuntu): 
Выполните вход на свой удаленный сервер

Установите docker на сервер:

    sudo apt install docker.io 

Установите docker-compose на сервер:

    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:

    scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml

    scp nginx.conf <username>@<host>:/home/<username>/nginx.conf

Cоздайте .env файл и впишите:

    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>

Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
  
   DOCKER_PASSWORD=<пароль от DockerHub>
   DOCKER_USERNAME=<имя пользователя>

    SECRET_KEY=<секретный ключ проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>

### Workflow состоит из четырёх шагов:

 1. Проверка кода на соответствие PEP8
 2. Сборка и публикация образа бекенда на DockerHub.
 3. Автоматический деплой на удаленный сервер.
 4. Отправка уведомления в телеграм-чат.

**На сервере соберите docker-compose:**

    sudo docker compose up -d --build

После успешной сборки на сервере выполните команды *(только после первого деплоя)*:
Соберите статические файлы:

    sudo docker compose exec backend python manage.py collectstatic --noinput

Примените миграции:

    sudo docker compose exec backend python manage.py migrate --noinput

Загрузите ингридиенты в базу данных (необязательно):
sudo docker compose exec backend python manage.py loadmodels
Создать суперпользователя Django:

    sudo docker compose exec backend python manage.py createsuperuser

Проект будет доступен по вашему IP
