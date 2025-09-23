# WS commands

### Initial
**Request:** Create ws-connection

```Empty```

**Response:** 

```json
{
  "type": "data",
  "payload": {
    "data_type": "chats",
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
 - Сообщения отправляются только для последнего чата (того, который создан позже всех)
 - `type` [См. Ws Message type](models.md#ws-message-type)
 - `data_type` [См. Data type](models.md#data-type)
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
  "type": "data",
  "payload": {
    "data_type": "new_chat",
    "message": "Chat created successfully!",
    "result": "success"
  }
}
```
 - `type` [См. Ws Message type](models.md#ws-message-type)
 - `data_type` [См. Data type](models.md#data-type)
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
 - `data_type` [См. Data type](models.md#data-type)
 - `action` [См. Command Action](models.md#command-action)

**Response:**

```json
{
  "type": "data",
  "payload": {
    "data_type": "ai_response",
    "chat_id": 1,
    "content": "some ai response"
  }
}
```

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
 - `data_type` [См. Data type](models.md#data-type)
 - `action` [См. Command Action](models.md#command-action)

**Response:**
```json
{
  "type": "data",
  "payload": {
    "data_type": "messages",
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
 - `data_type` [См. Data type](models.md#data-type)
 - `messages` [См. Message](models.md#message)
