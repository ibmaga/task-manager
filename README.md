# Task Manager API
#### Описание проекта

Task Manager API - это RESTful API для управления задачами, разработанное с использованием FastAPI и SQLAlchemy. Проект предоставляет возможности аутентификации пользователей, создания, редактирования и удаления задач.

#### Технология

* Python
* FastAPI
* Pydantic
* PostgreSQL
* SQLAlchemy
* Alembic (Миграция базы данных)
* Redis
* Pytest
* JWT
* Logfire (Логирование)

#### Устоновка

1. Клонируйте репозиторий:  
git clone https://github.com/your-username/task-manager-api.git
<code>cd task-manager-api</code>

2. Создайте виртуальное окружение и активируйте его:  
<code>python -m venv .venv
.venv\Scripts\activate</code>

3. Установите зависимости:  
<code>pip install -r requirements.txt</code>

4. Создайте файл .env на основе .env.example:
<code>copy .env.example .env</code>
Отредактируйте файл .env, указав необходимые параметры.

#### Структура API

API содержит следующие основные эндпоинты:  

- /auth - авторизация и регистрация пользователей
- /users - управление пользователями
- /tasks - управление задачами

#### Работа с миграциями
Создание новой миграции: <code>alembic revision -m "описание_миграции"</code>
Применение всех миграций: <code>alembic upgrade head</code>
Применение конкретной миграции: <code>alembic upgrade <id_миграции></code>
Откат миграции: <code>alembic downgrade -1</code>
Чтобы пометить текущую версию БД без выполнения миграций: <code>alembic stamp head</code>

#### Разработка и тестирование
Для запуска тестов используйте команду: <code>pytest</code>
