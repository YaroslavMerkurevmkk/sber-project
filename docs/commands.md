# WS commands

### Initial
**Request:** Create ws-connection

```Empty```

**Response:** 

```json
{
  "type": "data",
  "payload": {
    "chats": [
      {
        "id": 2,
        "name": "some name 2",
        "messages": [
          {
            "id": 123,
            "content": "some message content",
            "author": 1,
            "links": "http://example.com"
          }
        ]
      },
      {
        "id": 1,
        "name": "some name 1"
      }
    ]
  }
}
```
 - Сообщения отправляются только для первого последнего чата (тот, кто создан позже всех)
 - `type` [См. Ws Message type](models.md#ws-message-type)
 - `chats` [См. Chat](models.md#chat)
 - `messages` [См. Message](models.md#message)

### Create new chat

**Request:**
```json
{
  "type": "command",
  "payload": {
    "action": "create_chat",
    "name": "new chat name"
  }
}
```
 - `type` [См. Ws Message type](models.md#ws-message-type)
 - `action` [См. Command Action](models.md#command-action)

**Response:**

```json
{
  "type": "notification",
  "payload": {
    "message": "Chat created successfully!",
    "result": "success"
  }
}
```
 - `type` [См. Ws Message type](models.md#ws-message-type)
 - `message` сообщение для уведомления
 - `result` [См. Alert type](models.md#alert-type)

### Create new message
**Request:**

```json
{
  "type": "command",
  "payload": {
    "action": "create_message",
    "chat_id": 1,
    "content": "some message content"
  }
}
```
 - `type` [См. Ws Message type](models.md#ws-message-type)
 - `action` [См. Command Action](models.md#command-action)

**Response:**

`?` - new message from AI

### Get messages (pagination)
**Request:**

```json
{
  "type": "command",
  "payload": {
    "action": "get_messages",
    "chat_id": 1,
    "last_ind": 20
  }
}
```
 - Если нужно получить сообщения с самого последнего, то `last_ind` указать `-1`
 - `type` [См. Ws Message type](models.md#ws-message-type)
 - `action` [См. Command Action](models.md#command-action)

**Response:**
```json
{
  "type": "data",
  "payload": {
    "chat_id": 1,
    "messages": [
      {
        "id": 123,
        "content": "some message content",
        "author": 1,
        "links": "http://example.com"
      }
    ]
  }
}
```
 - `type` [См. Ws Message type](models.md#ws-message-type)
 - `messages` [См. Message](models.md#message)
