# FastAPI Backend

Это серверное приложение, разработанное с использованием FastAPI, асинхронного Python-фреймворка, ориентированного на создание высокопроизводительных REST API. Проект использует SQLAlchemy и Alembic для работы с базой данных и миграций, а также контейнеризован с помощью Docker.

## 📌 Возможности

- Асинхронные REST API endpoints
- Работа с PostgreSQL через SQLAlchemy
- Миграции базы данных через Alembic
- Разделение по модулям (auth, users, profiles, etc.)
- Поддержка Docker-контейнеров
- Валидация данных через Pydantic

## 🚀 Стек технологий

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Pydantic](https://docs.pydantic.dev/)

## 📁 Структура проекта

├── app/ # Основной код приложения  
│ ├── core/ # Настройки, конфигурации, зависимости  
│ ├── api/ # FastAPI роутеры  
│ ├── dependencies/ # Зависимости  
│ ├── dto/ # Pydantic-схемы  
│ ├── repository/ # Работа с базой данных  
│ ├── services/ # Бизнес-логика  
│ ├── utils/ # Утилиты  
│ └── app.py # Точка входа  
├── alembic/ # Миграции базы данных  
├── Dockerfile # Docker-контейнер  
├── .env # Переменные окружения (не включён в git)  
├── requirements.txt # Python-зависимости  
└── README.md  

## ⚙️ Установка и запуск

### 1. Клонируйте репозиторий

```shell
git clone https://github.com/NutaEnjoyer/fast-api-backend.git
cd fast-api-backend 
```

```markdown
### 2. Создайте `.env` файл

Создайте `.env` файл, заполненный переменными окружения по примеру из `.env.example`.

### 3. Запуск с Docker
```
```shell
docker build -t fastapi-backend .
docker run -d -p 8000:8000 --env-file .env fastapi-backend
```

```markdown
### 4. Локальный запуск (без Docker)

Убедитесь, что у вас установлен Python 3.10+
```
```shell
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```markdown
## 🛠 Alembic миграции
```
```shell
# создать новую миграцию
alembic revision --autogenerate -m "create users table"```

# применить миграции
alembic upgrade head
```

```markdown
## 📬 API документация

После запуска приложения откройте в браузере:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📄 Лицензия

Проект распространяется под лицензией MIT.
```