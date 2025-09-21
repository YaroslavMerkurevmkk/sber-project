// //Interface

const roomName = JSON.parse(document.getElementById('chatname').innerHTML);

const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === "init") {
        const chatsDiv = document.getElementById("chats");
        data.chats.forEach(chat => {
            const el = document.createElement("div");
            el.innerHTML = el.title = `Chat: ${chat.name} (ID: ${chat.id})`;
            chatsDiv.appendChild(el);
        });
    }
};

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-input').focus();
document.querySelector('#chat-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};

// // Exit button warning

document.addEventListener("DOMContentLoaded", () =>{
    document.getElementById('exit-button').addEventListener('click', () => {
        Swal.fire({
            title: "Выход",
            text: "Вы уверены?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: '<a href="/logout">Да</a>',
            cancelButtonText: "Отмена",
        })
    });
});

// // Load chats

const chatListSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

chatListSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);
    if (data.type === "data" && data.payload && "chats" in data.payload) {
        const chatsDiv = document.getElementById("chats");
        data.payload.chats.forEach(chat => {
            const el = document.createElement("div");
            el.textContent = `Chat: ${chat.name} (ID: ${chat.id})`;
            chatsDiv.appendChild(el);
        });
    }
    if (data.type === "notification") {
        Swal.fire("Notification", data.payload.message, data.payload.result);
    }
};

// // Create chat

document.getElementById("create-chat-btn").addEventListener("click", () => {
    Swal.fire({
        title: "Создать новый чат",
        input: "text",
        inputLabel: "Введите название",
        showCancelButton: true,
        confirmButtonText: "Создать",
        cancelButtonText: "Отмена",
        inputValidator: (value) => {
            if (!value) {
                return "Название не может быть пустым!";
            }
        }
    }).then((result) => {
        if (result.isConfirmed) {
            chatSocket.send(JSON.stringify({
                type: "command",
                payload: {
                    action: "create_chat",
                    name: result.value
                }
            }));
        }
    });
});