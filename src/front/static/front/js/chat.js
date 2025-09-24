// //Interface

const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

let chatsDiv;
let chatDiv;
let sideDiv;
let chatNameDiv;

//States
let chats;
let cur_chat = 0;

WebSocket.onopen = function()
{
    chatSocket.send();
};

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let payload = data.payload;

    if (data.type === "notification")
    {
        Swal.fire({
            title: payload.message,
            icon: payload.result
        });

        return;
    }

    switch (payload.data_type)
    {
        case 'chats': //init
        {
            chats = payload.chats;
            if (chats.length === 0)
            {
                return;
            }

            cur_chat = chats[0].id;

            chats.forEach(chat => {
                if (!(messages in chat))
                    chat.messages = [];
                let el = document.createElement("div");
                el.classList.add('chats-item');
                el.dataset.id = `${chat.id}`;
                el.innerHTML = el.title = `${chat.name}`;
                chatsDiv.appendChild(el);
            });
            break;
        }
        case 'messages': //Load messages
        {
            chats.find((c) => c.id === payload.chat_id).unshift(data.messages);

            if (payload.chat_id != cur_chat)
                break;

            payload.messages.reverse();


            payload.messages.forEach((message) =>{
                let el = document.createElement("div");
                el.classList.add('chat-item');
                el.dataset.id = message.id;
                if (message.author == 0) //Agent
                    el.classList.add('ai-message');
                else
                    el.classList.add('human-message');
                el.innerHTML = message.content;

                chatsDiv.prepend(el);
            });
            break;
        }
        case 'ai_response': //Create message
        {
            chats.find((c) => c.id === payload.chat_id).append({
                author: 0,
                content: payload.content
            });
            if (cur_chat !== payload.chat_id)
                break;

            let el = document.createElement("div");
            el.classList.add('chat-item');
            // el.dataset.id = message.id;
            el.classList.add('ai-message');

            el.innerHTML = message.content;

            chatsDiv.appendChild(el);
            break;
        }
        case 'new_chat':
        {
            chats.append(payload.chat);
            openChat(payload.chat.id);
            break;
        }
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

//Functions

function loadMessages(chat, id)
{
    chatSocket.send(JSON.stringify({
        type: "command",
        payload: {
            action: "get_messages",
            chat: chat,
            last_ind: id
        }
    }));
}

function createChat()
{
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
}

function openChat(id)
{
    if (cur_chat == id)
        return;

    clearChat();

    const chat = chats.find((c) => c.id === id);

    chatNameDiv.innerHTML = chat.name;

    if (chat.messages.length == 0)
        loadMessages(id, -1);
    else
    {
        chat.messages.forEach((message) =>{
            let el = document.createElement("div");
            el.classList.add('chat-item');
            el.dataset.id = message.id;
            if (message.author == 0)
                el.classList.add('ai-message');
            else
                el.classList.add('human-message');
            el.innerHTML = message.content;

            chatsDiv.appendChild(el);
        });
    }

    cur_chat = id;
}

function clearChat()
{
    chatDiv.innerHTML = '';
}

function loadChat(id)
{
    const chat = chats.find((c) => c.id === id);
    chat.messages.forEach((message) =>{
        let el = document.createElement("div");
        el.classList.add('chat-item');
        el.dataset.id = message.id;
        if (message.author == 0) //Agent
            el.classList.add('ai-message');
        else
            el.classList.add('human-message');
        el.innerHTML = message.content;

        chatsDiv.prepend(el);
    });
}




// ------------------ Голосовой ввод ------------------
function startVoiceInput() {
    if (!('webkitSpeechRecognition' in window && 'SpeechRecognition' in window)) {
        Swal.fire({
            title: 'Ой!',
            text: 'Ваш браузер не поддерживает микрофон',
            icon: 'error'
        });
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'ru-RU';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.start();

    recognition.onresult = function(event) {
        const speechResult = event.results[0][0].transcript;
        document.getElementById('chat-input').value = speechResult;
    };
}

// ------------------ Голосовой вывод ------------------
function speakText(text) {
    if (!('speechSynthesis' in window)) return;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ru-RU';
    speechSynthesis.speak(utterance);
}



//Load document

document.addEventListener("DOMContentLoaded", () =>{

    chatsDiv = document.getElementById("chats");
    chatDiv = document.getElementById("chat");
    chatNameDiv = document.getElementById("chatname");
    sideDiv = document.querySelector(".sidebar");

    //Events
    document.getElementById('exit-button').addEventListener('click', () => {
        Swal.fire({
            title: "Выход",
            text: "Вы уверены?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: '<a href="/logout">Выход</a>',
            cancelButtonText: "Отмена",
        })
    });

    document.querySelector('.chat-scroll').addEventListener('scroll', () => {
        const rectItem = document.querySelector('.chat-item').getBoundingClientRect();
        const rect = document.querySelector('.chat-wrapper').getBoundingClientRect();


        //First item is visible
        if (rect.top < rectItem.top)
            loadMessages(cur_chat, chat);
    });

    document.getElementById('menu-button').addEventListener('click', () => {
        sideDiv.classList.toggle("sidebar-open");
    });

    const input = document.getElementById('chat-input');
    const submit = document.getElementById('chat-message-submit');

    input.focus();
    input.onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            submit.click();
        }
    };

    submit.onclick = function(e) {
        chatSocket.send(JSON.stringify({
            type: "command",
            payload: {
                action: "create_message",
                "chat_id": current_chat
            }
        }));
        input.value = '';
    };

    document.getElementById('chat-speak-message').addEventListener('click', (e) => {
        startVoiceInput();
    });

    document.getElementById('chats').addEventListener('click', (e) => {
        let target = e.target.closest('.chats-item');

        if (!target)
            return;

        openChat(target.dataset.id);
    });

    document.getElementById("create-chat-btn").addEventListener("click", createChat);
});
