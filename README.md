# TGAdminPanel

## English Description

TGAdminPanel is a powerful web application designed for efficient management of Telegram channel content. It provides a user-friendly interface to organize your Telegram channels into groups, create and schedule posts with text and images, and automate publishing processes. Whether you're managing multiple channels or need to plan content in advance, TGAdminPanel streamlines your workflow with robust backend processing and real-time updates.

### Key Features
- **Channel Management**: Organize channels into groups for better organization
- **Content Creation**: Create posts with rich text and image support
- **Scheduling**: Schedule posts for future publication or publish immediately
- **Asynchronous Processing**: Powered by Celery for reliable task handling
- **Modern UI**: Built with React and TypeScript for a responsive experience
- **Docker Support**: Easy deployment with Docker Compose

### Tech Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, TypeScript, Tailwind CSS
- **Task Queue**: Celery with Redis
- **Deployment**: Docker, Docker Compose

## Описание на русском

TGAdminPanel - мощное веб-приложение, предназначенное для эффективного управления контентом Telegram-каналов. Оно предоставляет удобный интерфейс для организации ваших Telegram-каналов в группы, создания и планирования постов с текстом и изображениями, а также автоматизации процессов публикации. Независимо от того, управляете ли вы несколькими каналами или нуждаетесь в предварительном планировании контента, TGAdminPanel упрощает вашу работу с надежной обработкой на backend и обновлениями в реальном времени.

### Ключевые особенности
- **Управление каналами**: Организация каналов в группы для лучшей организации
- **Создание контента**: Создание постов с поддержкой текста и изображений
- **Планирование**: Планирование постов на будущее или публикация немедленно
- **Асинхронная обработка**: Работает на Celery для надежной обработки задач
- **Современный UI**: Построен на React и TypeScript для отзывчивого опыта
- **Поддержка Docker**: Легкое развертывание с Docker Compose

### Стек технологий
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, TypeScript, Tailwind CSS
- **Очередь задач**: Celery с Redis
- **Развертывание**: Docker, Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alex-lik/TGAdminPanel.git
   cd TGAdminPanel
   ```

2. Copy environment files:
   ```bash
   cp .env.example .env
   cp backend/app/.env.example backend/app/.env
   ```

3. Configure your environment variables in `.env` files.

4. Start the application with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Usage

- Access the web interface at `http://localhost:3000`
- Create channel groups and add your Telegram channels with bot tokens
- Create posts with content for specific channels
- Schedule posts or publish immediately
- Monitor publishing status through the dashboard

## Configuration

Copy `.env.example` to `.env` and adjust values. `VITE_API_BASE_URL` sets the address of the backend API and is passed to the frontend during the docker build.