# Enums

### Message Author
 - `0` - Agent
 - `1` - Human

### Ws message type
 - `command` - команда
 - `data` - данные
 - `notification` - уведомление

### Data type
 - `chats` - все чаты пользователя
 - `new_chat` - новый чат
 - `ai_response` - ответ от агента, за запрос от пользователя
 - `messages` - сообщения для чата (пагинация)

### Command action
 - `create_chat` - создать чат
 - `create_message` - создать сообщение
 - `get_messages` - получить сообщения (пагинация)

### Alert type
Аналогичны типам уведомлений в `Sweetalert`
 - `success` - успех
 - `warning` - некритичная ошибка
 - `info` - информация
 - `question` - вопрос
 - `error` - ошибка


# Database models

### Message
```json
{
  "id": 123,
  "content": "some message content",
  "author": 1,
  "links": "http://example.com"
}
```
 - `id`: (`int`) - идентификатор сообщения 
 - `content`: (`string`) - контент сообщения
 - `author`: ([Message Author](#message-author)) - автор сообщения
 - `links`: (`string`) - ссылки на ресурсы


### Chat
```json
{
  "id": 1,
  "name": "some name 1",
  "messages": []
}
```
 - `id`: (`int`) - идентификатор чата 
 - `name`: (`string`) - имя чата
 - `messages`: (`Optional[array of objects]`[Message](#message)) - сообщения

