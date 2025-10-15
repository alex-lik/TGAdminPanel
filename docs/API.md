# Документация API TGAdminPanel
__________________________________________________________________________________________________________________________________________________

## Обзор

TGAdminPanel предоставляет REST API для управления контентом Telegram-каналов. API позволяет создавать группы каналов, добавлять каналы и планировать публикацию постов.

Базовый URL: `http://localhost:8000/api` (с префиксом /api)
__________________________________________________________________________________________________________________________________________________

## Аутентификация

API защищен Basic Authentication. Все запросы должны содержать заголовок Authorization.

Пример заголовка:
```
Authorization: Basic dXNlcjpwYXNzd29yZA==
```

Где `dXNlcjpwYXNzd29yZA==` - это base64-кодированная строка `username:password`.
__________________________________________________________________________________________________________________________________________________

## Группы каналов

### Получить все группы каналов

**Эндпоинт:** `GET /api/channel-groups/`
**Описание:** Возвращает список всех групп каналов с их каналами

**Пример curl:**
```bash
curl -X GET "http://localhost:8000/api/channel-groups/" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA=="
```

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Python Hacks",
    "channels": [
      {
        "id": 1,
        "name": "py hack ru",
        "channel_id": "1002825801123ru",
        "bot_token": "123456:ABC...",
        "language": "ru"
      }
    ]
  }
]
```


__________________________________________________________________________________________________________________________________________________

### Создать группу каналов

**Эндпоинт:** `POST /api/channel-groups/`
**Описание:** Создает новую группу каналов

**Пример curl:**
```bash
curl -X POST "http://localhost:8000/api/channel-groups/" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA==" \
  -H "Content-Type: application/json" \
  -d '{"name": "Новая группа"}'
```

**Ответ:**
```json
{
  "id": 2,
  "name": "Новая группа",
  "channels": []
}
```
__________________________________________________________________________________________________________________________________________________

### Получить группу каналов по ID

**Эндпоинт:** `GET /api/channel-groups/{group_id}`
**Описание:** Возвращает конкретную группу каналов

**Пример curl:**
```bash
curl -X GET "http://localhost:8000/api/channel-groups/1" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA=="
```

### Удалить группу каналов

**Эндпоинт:** `DELETE /api/channel-groups/{group_id}`
**Описание:** Удаляет группу каналов и все ее каналы

**Пример curl:**
```bash
curl -X DELETE "http://localhost:8000/api/channel-groups/1" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA=="
```

**Ответ:**
```json
{
  "message": "Channel group deleted"
}
```
__________________________________________________________________________________________________________________________________________________

## Каналы

### Добавить канал в группу

**Эндпоинт:** `POST /api/channel-groups/{group_id}/channels/`
**Описание:** Добавляет канал в указанную группу

**Пример curl:**
```bash
curl -X POST "http://localhost:8000/api/channel-groups/1/channels/" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA==" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "py hack ua",
    "channel_id": "1002531660864ua",
    "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    "language": "ua"
  }'
```
__________________________________________________________________________________________________________________________________________________

### Удалить канал

**Эндпоинт:** `DELETE /api/channels/{channel_id}`
**Описание:** Удаляет канал по его ID

**Пример curl:**
```bash
curl -X DELETE "http://localhost:8000/api/channels/1" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA=="
```

**Ответ:**
```json
{
  "message": "Channel deleted"
}
```
__________________________________________________________________________________________________________________________________________________

## Посты

### Получить все посты

**Эндпоинт:** `GET /api/posts/`
**Описание:** Возвращает список всех постов

**Пример curl:**
```bash
curl -X GET "http://localhost:8000/api/posts/" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA=="
```

**Ответ:**
```json
[
  {
    "id": 1,
    "group_id": 1,
    "publish_time": "2023-10-13T12:00:00",
    "status": "published",
    "created_at": "2023-10-13T10:00:00",
    "contents": [
      {
        "id": 1,
        "channel_id": 1,
        "content": "Привет мир!"
      }
    ]
  }
]
```
__________________________________________________________________________________________________________________________________________________

### Создать пост

**Эндпоинт:** `POST /api/posts/`
**Описание:** Создает новый пост для публикации

**Пример curl:**
```bash
curl -X POST "http://localhost:8000/api/posts/" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA==" \
  -H "Content-Type: application/json" \
  -d '{
    "group_id": 1,
    "publish_time": "2023-10-14T10:00:00",
    "publish_now": false,
    "contents": [
      {
        "channel_id": 2,
        "content": "Пост для py hack ua"
      }
    ]
  }'
```

**Ответ:**
```json
{
  "id": 2,
  "group_id": 1,
  "publish_time": "2023-10-14T10:00:00",
  "status": "scheduled",
  "created_at": "2023-10-13T10:00:00",
  "contents": [
    {
      "id": 3,
      "channel_id": 2,
      "content": "Пост для py hack ua"
    }
  ]
}
```
__________________________________________________________________________________________________________________________________________________

### Получить пост по ID

**Эндпоинт:** `GET /api/posts/{post_id}`
**Описание:** Возвращает конкретный пост

**Пример curl:**
```bash
curl -X GET "http://localhost:8000/api/posts/1" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA=="
```

### Удалить пост

**Эндпоинт:** `DELETE /api/posts/{post_id}`
**Описание:** Удаляет пост по его ID

**Пример curl:**
```bash
curl -X DELETE "http://localhost:8000/api/posts/1" \
  -H "Authorization: Basic dXNlcjpwYXNzd29yZA=="
```

**Ответ:**
```json
{
  "message": "Post deleted"
}
```
__________________________________________________________________________________________________________________________________________________

## Модели данных

### ChannelGroup
- `id` (integer): Уникальный идентификатор
- `name` (string): Название группы
- `channels` (array): Список каналов в группе

### Channel
- `id` (integer): Уникальный идентификатор
- `name` (string): Название канала
- `channel_id` (string): ID канала в Telegram (например, "1002531660864ua")
- `bot_token` (string): Токен Telegram бота
- `language` (string, опционально): Язык канала

### Post
- `id` (integer): Уникальный идентификатор
- `group_id` (integer): ID группы каналов
- `publish_time` (datetime): Время публикации
- `status` (string): Статус ("scheduled", "published", "failed")
- `created_at` (datetime): Время создания
- `contents` (array): Список контента для разных каналов

### PostContent
- `id` (integer): Уникальный идентификатор
- `channel_id` (integer): ID целевого канала
- `content` (string): Текстовый контент поста
- `message_id` (integer, опционально): ID сообщения в Telegram после публикации
- `image_path` (string, опционально): Путь к файлу изображения

## Обработка ошибок

API возвращает стандартные HTTP коды статусов:
- `200`: Успех
- `401`: Неавторизован
- `404`: Ресурс не найден
- `422`: Ошибка валидации
- `500`: Внутренняя ошибка сервера

Ответы с ошибками содержат JSON объект с сообщением об ошибке:
```json
{
  "detail": "Сообщение об ошибке"
}
```

## Примечания

- Все поля datetime в формате ISO 8601
- Флаг `publish_now` в создании поста немедленно запускает публикацию через Celery
- Посты с `publish_now: false` планируются для будущей публикации
- Поддержка изображений запланирована, но не полностью реализована в текущей версии