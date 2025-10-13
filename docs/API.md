# API Documentation for TGAdminPanel

## Overview

TGAdminPanel provides a REST API for managing Telegram channel content. The API allows you to create channel groups, add channels, and schedule posts for publication.

Base URL: `http://localhost:8000` (default for backend)

## Authentication

Currently, the API does not require authentication. All endpoints are open.

## Endpoints

### Channel Groups

#### GET /channel-groups/
Get all channel groups.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Main Channels",
    "channels": [
      {
        "id": 1,
        "name": "Channel 1",
        "channel_id": "@channel1",
        "bot_token": "123456:ABC...",
        "language": "en"
      }
    ]
  }
]
```

**Examples:**
```bash
curl -X GET "http://localhost:8000/channel-groups/"
```

```python
import requests

response = requests.get("http://localhost:8000/channel-groups/")
groups = response.json()
```

```javascript
fetch('http://localhost:8000/channel-groups/')
  .then(response => response.json())
  .then(data => console.log(data));
```

#### POST /channel-groups/
Create a new channel group.

**Request Body:**
```json
{
  "name": "New Group"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "New Group",
  "channels": []
}
```

**Examples:**
```bash
curl -X POST "http://localhost:8000/channel-groups/" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Group"}'
```

```python
import requests

data = {"name": "New Group"}
response = requests.post("http://localhost:8000/channel-groups/", json=data)
group = response.json()
```

```javascript
fetch('http://localhost:8000/channel-groups/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ name: 'New Group' })
})
.then(response => response.json())
.then(data => console.log(data));
```

#### GET /channel-groups/{group_id}
Get a specific channel group by ID.

**Parameters:**
- `group_id` (integer): The ID of the channel group

**Response:**
```json
{
  "id": 1,
  "name": "Main Channels",
  "channels": [...]
}
```

**Examples:**
```bash
curl -X GET "http://localhost:8000/channel-groups/1"
```

```python
import requests

response = requests.get("http://localhost:8000/channel-groups/1")
group = response.json()
```

```javascript
fetch('http://localhost:8000/channel-groups/1')
  .then(response => response.json())
  .then(data => console.log(data));
```

#### DELETE /channel-groups/{group_id}
Delete a channel group and all its channels.

**Parameters:**
- `group_id` (integer): The ID of the channel group to delete

**Response:**
```json
{
  "message": "Channel group deleted"
}
```

**Examples:**
```bash
curl -X DELETE "http://localhost:8000/channel-groups/1"
```

```python
import requests

response = requests.delete("http://localhost:8000/channel-groups/1")
print(response.json())
```

```javascript
fetch('http://localhost:8000/channel-groups/1', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

### Channels

#### POST /channel-groups/{group_id}/channels/
Add a channel to a specific group.

**Parameters:**
- `group_id` (integer): The ID of the channel group

**Request Body:**
```json
{
  "name": "My Channel",
  "channel_id": "@mychannel",
  "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
  "language": "en"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "My Channel",
  "channel_id": "@mychannel",
  "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
  "language": "en"
}
```

**Examples:**
```bash
curl -X POST "http://localhost:8000/channel-groups/1/channels/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Channel",
    "channel_id": "@mychannel",
    "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    "language": "en"
  }'
```

```python
import requests

data = {
    "name": "My Channel",
    "channel_id": "@mychannel",
    "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    "language": "en"
}
response = requests.post("http://localhost:8000/channel-groups/1/channels/", json=data)
channel = response.json()
```

```javascript
fetch('http://localhost:8000/channel-groups/1/channels/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'My Channel',
    channel_id: '@mychannel',
    bot_token: '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11',
    language: 'en'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

#### DELETE /channels/{channel_id}
Delete a channel.

**Parameters:**
- `channel_id` (integer): The ID of the channel to delete

**Response:**
```json
{
  "message": "Channel deleted"
}
```

**Examples:**
```bash
curl -X DELETE "http://localhost:8000/channels/1"
```

```python
import requests

response = requests.delete("http://localhost:8000/channels/1")
print(response.json())
```

```javascript
fetch('http://localhost:8000/channels/1', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

### Posts

#### GET /posts/
Get all posts.

**Response:**
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
        "content": "Hello World!"
      }
    ]
  }
]
```

**Examples:**
```bash
curl -X GET "http://localhost:8000/posts/"
```

```python
import requests

response = requests.get("http://localhost:8000/posts/")
posts = response.json()
```

```javascript
fetch('http://localhost:8000/posts/')
  .then(response => response.json())
  .then(data => console.log(data));
```

#### POST /posts/
Create a new post.

**Request Body:**
```json
{
  "group_id": 1,
  "publish_time": "2023-10-13T12:00:00",
  "publish_now": false,
  "contents": [
    {
      "channel_id": 1,
      "content": "Hello from channel 1!"
    },
    {
      "channel_id": 2,
      "content": "Hello from channel 2!"
    }
  ]
}
```

**Response:**
```json
{
  "id": 2,
  "group_id": 1,
  "publish_time": "2023-10-13T12:00:00",
  "status": "scheduled",
  "created_at": "2023-10-13T10:00:00",
  "contents": [
    {
      "id": 3,
      "channel_id": 1,
      "content": "Hello from channel 1!"
    },
    {
      "id": 4,
      "channel_id": 2,
      "content": "Hello from channel 2!"
    }
  ]
}
```

**Examples:**
```bash
curl -X POST "http://localhost:8000/posts/" \
  -H "Content-Type: application/json" \
  -d '{
    "group_id": 1,
    "publish_time": "2023-10-13T12:00:00",
    "publish_now": false,
    "contents": [
      {
        "channel_id": 1,
        "content": "Hello from channel 1!"
      }
    ]
  }'
```

```python
import requests

data = {
    "group_id": 1,
    "publish_time": "2023-10-13T12:00:00",
    "publish_now": False,
    "contents": [
        {
            "channel_id": 1,
            "content": "Hello from channel 1!"
        }
    ]
}
response = requests.post("http://localhost:8000/posts/", json=data)
post = response.json()
```

```javascript
fetch('http://localhost:8000/posts/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    group_id: 1,
    publish_time: '2023-10-13T12:00:00',
    publish_now: false,
    contents: [
      {
        channel_id: 1,
        content: 'Hello from channel 1!'
      }
    ]
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

#### GET /posts/{post_id}
Get a specific post by ID.

**Parameters:**
- `post_id` (integer): The ID of the post

**Response:**
```json
{
  "id": 1,
  "group_id": 1,
  "publish_time": "2023-10-13T12:00:00",
  "status": "published",
  "created_at": "2023-10-13T10:00:00",
  "contents": [...]
}
```

**Examples:**
```bash
curl -X GET "http://localhost:8000/posts/1"
```

```python
import requests

response = requests.get("http://localhost:8000/posts/1")
post = response.json()
```

```javascript
fetch('http://localhost:8000/posts/1')
  .then(response => response.json())
  .then(data => console.log(data));
```

#### DELETE /posts/{post_id}
Delete a post.

**Parameters:**
- `post_id` (integer): The ID of the post to delete

**Response:**
```json
{
  "message": "Post deleted"
}
```

**Examples:**
```bash
curl -X DELETE "http://localhost:8000/posts/1"
```

```python
import requests

response = requests.delete("http://localhost:8000/posts/1")
print(response.json())
```

```javascript
fetch('http://localhost:8000/posts/1', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

## Data Models

### ChannelGroup
- `id` (integer): Unique identifier
- `name` (string): Group name
- `channels` (array): List of channels in the group

### Channel
- `id` (integer): Unique identifier
- `name` (string): Channel name
- `channel_id` (string): Telegram channel ID (e.g., "@mychannel")
- `bot_token` (string): Telegram bot token
- `language` (string, optional): Channel language

### Post
- `id` (integer): Unique identifier
- `group_id` (integer): ID of the channel group
- `publish_time` (datetime): Scheduled publication time
- `status` (string): Post status ("scheduled", "published", "failed")
- `created_at` (datetime): Creation timestamp
- `contents` (array): List of post contents for different channels

### PostContent
- `id` (integer): Unique identifier
- `channel_id` (integer): ID of the target channel
- `content` (string): Text content for the post
- `message_id` (integer, optional): Telegram message ID after publication
- `image_path` (string, optional): Path to image file

## Error Handling

The API returns standard HTTP status codes:
- `200`: Success
- `404`: Resource not found
- `422`: Validation error
- `500`: Internal server error

Error responses include a JSON object with an error message:
```json
{
  "detail": "Error message"
}
```

## Notes

- All datetime fields are in ISO 8601 format
- The `publish_now` flag in post creation immediately triggers publication via Celery
- Posts with `publish_now: false` are scheduled for future publication
- Image support is planned but not fully implemented in the current version