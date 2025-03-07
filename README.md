# Курсовая работа

Этот проект реализует Django приложение с полной контейнеризацией и настроенным CI/CD пайплайном.

## Структура проекта


```
.
├── .github/workflows       # CI/CD конфигурация для GitHub Actions
├── app                     # Директория с Django приложением
├── nginx                   # Конфигурация Nginx
│   ├── conf                # Конфигурационные файлы Nginx
│   └── ssl                 # SSL сертификаты
├── scripts                 # Вспомогательные скрипты
├── .env.example            # Пример файла переменных окружения
├── docker-compose.yml      # Конфигурация Docker Compose для локальной разработки
├── docker-compose.prod.yml # Конфигурация Docker Compose для продакшена
├── Dockerfile.django       # Dockerfile для Django приложения
└── README.md               # Документация проекта
```

## Компоненты

- **Django** - бэкенд веб-приложения
- **PostgreSQL** - база данных
- **Redis** - кэш и брокер сообщений для Celery
- **Celery** - асинхронная обработка задач
- **Nginx** - веб-сервер и прокси
- **Docker** - контейнеризация
- **GitHub Actions** - CI/CD

## Локальный запуск проекта

### Предварительные требования

- Установленный Docker и Docker Compose
- Git

### Шаги по запуску

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Ferrum76/cource-7.git
   cd cource-7
   ```
2. Создайте файл .env из примера:
    ```bash
    cp .env.sample .env
    ```
3. Отредактируйте файл .env вставив необходимые значения.
4. Убедитесь, что скрипт entrypoint.sh имеет права на выполнение:
    ```bash
    chmod +x scripts/entrypoint.sh
    ```
5. Запустите проект:
    ```bash
    docker-compose up -d
    ```
6. Проект будет доступен по адресу http://localhost


## Настройка CI/CD
### Настройка GitHub Secrets
В настройках GitHub репозитория необходимо добавить следующие секреты:

- `DOCKER_USERNAME` - имя пользователя Docker Hub
- `DOCKER_PASSWORD` - пароль пользователя Docker Hub
- `SSH_PRIVATE_KEY` - приватный SSH-ключ для доступа к серверу
- `PRODUCTION_HOST` - адрес продакшн сервера
- `PRODUCTION_USER` - пользователь для подключения к серверу
- Все переменные окружения из файла `.env`

## Настройка сервера для деплоя

###  Установите Docker и Docker Compose на сервер:
```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
```

### Добавление текущего пользователя в группу docker
```bash
sudo usermod -aG docker ${USER}
```

### Установка Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Настройте SSH-доступ для GitHub Actions:

### Создайте папку .ssh и файл authorized_keys если они не существуют:

```bash
mkdir -p ~/.ssh
touch ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### Добавьте публичный ключ, соответствующий приватному ключу, добавленному в GitHub Secrets, в файл ~/.ssh/authorized_keys.

Подготовьте директорию для проекта:
```bash
mkdir -p ~/app/nginx/conf
mkdir -p ~/app/nginx/ssl
```



## Процесс CI/CD

1. При пуше в ветку develop запускаются тесты и линтинг кода
2. При успешном прохождении тестов происходит сборка Docker образов
3. При пуше в ветку main, после сборки образов, происходит деплой на продакшн-сервер

## Дополнительная информация
### Управление базой данных
1. Для создания резервной копии базы данных:
    ```bash
    docker-compose exec db pg_dump -U django_user django_db > backup.sql
    ```
2. Для восстановления базы данных из резервной копии:
    ```bash
    cat backup.sql | docker-compose exec -T db psql -U django_user django_db
    ```
### Логи сервисов
1. Для просмотра логов всех сервисов:
    ```bash
    docker-compose logs
    ```
2. Для просмотра логов конкретного сервиса (например, Django):
    ```bash
    docker-compose logs web
    ```

### Обновление проекта вручную
Если требуется обновить проект вручную на сервере:
```bash
cd ~/app
git pull
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

## Особенности проекта
- Автоматическое ожидание готовности базы данных перед запуском Django
- Автоматическое применение миграций
- Автоматический сбор статических файлов
- Настроенный HTTPS с перенаправлением HTTP на HTTPS
- Управление асинхронными задачами через Celery
- Полная изоляция сервисов в отдельных контейнерах