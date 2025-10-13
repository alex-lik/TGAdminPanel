# TGAdminPanel - Документация проекта

## Обзор

TGAdminPanel - это мощное веб-приложение для эффективного управления контентом Telegram-каналов. Оно предоставляет удобный интерфейс для организации Telegram-каналов в группы, создания и планирования постов с текстом и изображениями, а также автоматизации процессов публикации.

## Архитектура системы

### Компоненты

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React + TS)  │◄──►│   (FastAPI)     │◄──►│   (SQLite)      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   REST API      │    │   SQLAlchemy    │
│   (Vite)        │    │   (HTTP)        │    │   (ORM)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Task Queue    │    │   Publisher     │    │   Telegram API  │
│   (Celery)      │◄──►│   (httpx)       │◄──►│   (Bot API)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲
         │
┌─────────────────┐
│   Redis         │
│   (Message      │
│    Broker)      │
└─────────────────┘
```

### Backend (FastAPI)

- **Основной фреймворк**: FastAPI для создания REST API
- **База данных**: SQLAlchemy с SQLite (можно заменить на PostgreSQL)
- **Асинхронная обработка**: Celery для фоновых задач
- **Внешние API**: httpx для запросов к Telegram Bot API
- **Логирование**: Loguru для структурированного логирования

### Frontend (React + TypeScript)

- **UI фреймворк**: React 19 с TypeScript
- **Стилизация**: Tailwind CSS для современных компонентов
- **HTTP клиент**: Axios для API запросов
- **Роутинг**: React Router для навигации
- **Сборка**: Vite для быстрой разработки

### Task Queue (Celery)

- **Брокер сообщений**: Redis для хранения задач
- **Планировщик**: Celery Beat для периодических задач
- **Обработка публикаций**: Асинхронная отправка постов в Telegram

### Database Schema

```
ChannelGroup
├── id (PK)
├── name
└── channels (relationship)

Channel
├── id (PK)
├── group_id (FK)
├── name
├── channel_id
├── bot_token
└── language

Post
├── id (PK)
├── group_id (FK)
├── publish_time
├── status
├── created_at
└── contents (relationship)

PostContent
├── id (PK)
├── post_id (FK)
├── channel_id (FK)
├── content
├── message_id
└── image_path
```

## Установка и настройка

### Предварительные требования

- Docker и Docker Compose
- Git

### Быстрый старт

1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com/alex-lik/TGAdminPanel.git
   cd TGAdminPanel
   ```

2. **Настройка переменных окружения:**
   ```bash
   cp .env.example .env
   cp backend/app/.env.example backend/app/.env
   ```

3. **Запуск с Docker:**
   ```bash
   docker-compose up --build
   ```

4. **Доступ к приложению:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API документация: http://localhost:8000/docs

### Ручная установка

#### Backend

1. **Создание виртуального окружения:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

2. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка переменных окружения:**
   ```bash
   cp app/.env.example app/.env
   # Отредактируйте .env файл
   ```

4. **Запуск Redis:**
   ```bash
   redis-server
   ```

5. **Запуск Celery:**
   ```bash
   celery -A app.celery_app worker --loglevel=info
   celery -A app.celery_app beat --loglevel=info
   ```

6. **Запуск сервера:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Frontend

1. **Установка зависимостей:**
   ```bash
   cd frontend/app
   npm install
   ```

2. **Запуск в режиме разработки:**
   ```bash
   npm run dev
   ```

3. **Сборка для продакшена:**
   ```bash
   npm run build
   ```

## Конфигурация

### Переменные окружения

#### Backend (.env)

```env
# Database
SQLALCHEMY_DATABASE_URL=sqlite:///./telegram_content.db

# Logging
LOG_PATH=./logs/today.log

# Publisher URL (для внешнего сервиса публикации)
PUBLISHER_URL=http://10.0.15.4:8012/publish
```

#### Frontend (.env)

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000
```

### Настройка Telegram ботов

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Добавьте бота как администратора в канал
4. Используйте токен и @username канала при добавлении канала в приложение

## Использование

### Создание группы каналов

1. Перейдите в раздел "Настройки"
2. Нажмите "Создать группу каналов"
3. Введите название группы

### Добавление канала

1. Выберите группу каналов
2. Нажмите "Добавить канал"
3. Заполните:
   - Название канала
   - ID канала (@username)
   - Токен бота
   - Язык (опционально)

### Создание поста

1. Перейдите в раздел "Контент"
2. Выберите группу каналов
3. Введите текст для каждого канала
4. Выберите время публикации или отметьте "Опубликовать сейчас"
5. Нажмите "Опубликовать"

### Просмотр истории постов

- Все созданные посты отображаются в разделе "История постов"
- Статусы: запланирован, опубликован, ошибка

## API

Подробная документация API доступна в файле [API.md](API.md).

## Разработка

### Структура проекта

```
TGAdminPanel/
├── backend/
│   ├── app/
│   │   ├── main.py          # Точка входа FastAPI
│   │   ├── models.py        # SQLAlchemy модели
│   │   ├── schemas.py       # Pydantic схемы
│   │   ├── crud.py          # CRUD операции
│   │   ├── database.py      # Настройки БД
│   │   ├── config.py        # Конфигурация
│   │   ├── celery_app.py    # Настройки Celery
│   │   ├── routes/          # API маршруты
│   │   ├── tasks.py         # Celery задачи
│   │   ├── sender.py        # Отправка в Telegram
│   │   └── publisher.py     # Публикация постов
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── src/
│   │   │   ├── App.tsx      # Главный компонент
│   │   │   ├── main.tsx     # Точка входа
│   │   │   └── ...
│   │   ├── package.json
│   │   └── Dockerfile
│   └── docker-compose.yml
├── docs/                    # Документация
├── docker-compose.yml       # Основной compose файл
└── README.md
```

### Добавление новых функций

1. **Backend:**
   - Добавьте модель в `models.py`
   - Создайте схему в `schemas.py`
   - Реализуйте CRUD в `crud.py`
   - Добавьте маршрут в `routes/`
   - Создайте задачу в `tasks.py` если нужно

2. **Frontend:**
   - Добавьте API функции в `App.tsx`
   - Создайте UI компоненты
   - Обновите состояние приложения

### Тестирование

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend/app
npm test
```

## Развертывание

### Docker Compose (рекомендуется)

```bash
docker-compose up -d --build
```

### Продакшен настройки

1. Замените SQLite на PostgreSQL
2. Настройте Nginx как reverse proxy
3. Включите HTTPS
4. Настройте мониторинг и логирование

## Устранение неполадок

### Распространенные проблемы

1. **Ошибка подключения к Telegram:**
   - Проверьте токен бота
   - Убедитесь, что бот добавлен в канал как администратор

2. **Задачи Celery не выполняются:**
   - Проверьте, что Redis запущен
   - Проверьте логи Celery worker

3. **Ошибка CORS:**
   - Проверьте настройки CORS в `main.py`

### Логи

- Backend логи: `backend/app/logs/`
- Celery логи: в консоли или настроить файл

## Лицензия

MIT License

## Контакты

- Автор: Alex Lik
- Репозиторий: https://github.com/alex-lik/TGAdminPanel