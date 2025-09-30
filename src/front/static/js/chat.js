const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const chatSocket = new WebSocket(protocol + window.location.host + '/ws/chat/');
const md2html = new showdown.Converter();

let t_delBtn;
let chatsDiv;
let chatDiv;
let sideDiv;
let chatNameDiv;
let submitBtn;

//States
let chats;
let cur_chat = -1;
let isInputEnabled = true;

WebSocket.onopen = function()
{
    chatSocket.send();
};

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    console.log(data);
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

            chats.forEach(chat => {
                chat.enabled = true;
                addChat(chat);
            });

            openChat(chats[0].id);
            break;
        }
        case 'messages': //Load messages
        {
            let chat = chats.find((c) => c.id === payload.chat_id);
            console.log(chat.messages);
            chat.messages = payload.messages.concat(chat.messages);

            if (payload.chat_id != cur_chat)
                break;

            payload.messages.reverse();

            let isEmpty = chatDiv.childNodes.length == 0;

            prependMessages(payload.messages);

            if (isEmpty)
                scrollToEnd();
            break;
        }
        case 'ai_response': //Create message
        {
            let chat = chats.find((c) => c.id === payload.chat_id);
            chat.enabled = true;
            chat.messages.push({
                author: 0,
                content: payload.content
            });
            if (cur_chat !== payload.chat_id)
                break;

            chatDiv.appendChild(formMessage({content: payload.content, author: 0, id: -1}));
            submitBtn.disabled = false;
            scrollToEnd();
            break;
        }
        case 'new_chat':
        {
            payload.chat.enabled = true;
            addChat(payload.chat, true);
            chats.push(payload.chat);
            openChat(payload.chat.id);
            break;
        }
        case 'deleted_chat':
        {
            chatsDiv.childNodes.find(n => n.dataset.id == payload.chat_id).remove();
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
            chat_id: chat,
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

    if (cur_chat != -1)
    {
        const oldChatNode = chatsDiv.querySelector(`div[data-id=\"${cur_chat}\"]`);
        oldChatNode.classList.remove('chat-selected');
    }

    clearChat();

    const chat = chats.find((c) => c.id === id);
    setInputEnabled(chat.enabled);
    const chatNode = chatsDiv.querySelector(`div[data-id=\"${id}\"]`);
    chatNode.classList.add('chat-selected');

    chatNameDiv.innerHTML = chat.name;

    if (chat.messages.length == 0)
        loadMessages(id, -1);
    else
    {
        appendMessages(chat.messages);
    }

    cur_chat = id;
    scrollToEnd();
}

function addChat(chat, reverse=false)
{
    if (!('messages' in chat))
        chat.messages = [];
    let el = document.createElement("div");
    el.classList.add('chats-item');
    el.dataset.id = `${chat.id}`;
    el.innerHTML = el.title = `${chat.name}`;

    let delbtn = t_delBtn.cloneNode(true);
    delbtn.addEventListener("click", onDeleteClick);
    delbtn.dataset.id = `${chat.id}`;

    el.appendChild(delbtn);
    if (reverse)
        chatsDiv.prepend(el);
    else
        chatsDiv.appendChild(el);
}

function formMessage(message)
{
    let el = document.createElement("div");
    el.classList.add('chat-item');
    el.dataset.id = message.id;
    if (message.author == 0) //Agent
        el.classList.add('ai-message');
    else
        el.classList.add('human-message');
    el.innerHTML = md2html.makeHtml(message.content);
    return el;
}

function appendMessages(messages)
{
    messages.forEach((message) =>{
        chatDiv.appendChild(formMessage(message));
    });
}

function prependMessages(messages)
{
    messages.forEach((message) =>{
        chatDiv.prepend(formMessage(message));
    });
}

function clearChat()
{
    chatDiv.innerHTML = '';
}

function loadChat(id)
{
    const chat = chats.find((c) => c.id === id);
    prependMessages(chat.messages);
}

function onDeleteClick(e) {
    let id = e.target.closest(".chats-item").dataset.id;
    Swal.fire({
        title: "Удалить чат",
        text: "Вы уверены?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Удалить',
        cancelButtonText: "Отмена",
    }).then(function(result){
        if(result.isConfirmed)
            deleteChat(id)
    });
}

function deleteChat(id)
{
    chatSocket.send(JSON.stringify({
        type: "command",
        payload: {
            action: "delete_chat",
            "chat_id": id
        }
    }));
}

function scrollToEnd()
{
    chatDiv.parentNode.scrollTop = chatDiv.parentNode.scrollHeight;
}

function setInputEnabled(enabled)
{
    isInputEnabled = enabled;
    submitBtn.classList.toggle('submit-disabled', enabled);
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
    t_delBtn = document.getElementById("t_dlt-button").content.querySelector(".del-button");

    //Events
    document.getElementById('exit-button').addEventListener('click', () => {
        Swal.fire({
            title: "Выход",
            text: "Вы уверены?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Выход',
            cancelButtonText: "Отмена",
        }).then(function(result){
            if(result.isConfirmed)
                window.location.href = "/logout";
        });
    });

    document.querySelector('.chat-scroll').addEventListener('scroll', () => {
        const rectItem = document.querySelector('.chat-item');
        const rect = document.querySelector('.chat-wrapper').getBoundingClientRect();


        //First item is visible
        if (rect.top < rectItem.getBoundingClientRect().top)
            loadMessages(cur_chat, parseInt(rectItem.dataset.id));
    });

    document.getElementById('menu-button').addEventListener('click', () => {
        sideDiv.classList.toggle("sidebar-open");
    });

    const input = document.getElementById('chat-input');
    submitBtn = document.getElementById('chat-message-submit');

    input.focus();
    input.onkeyup = function(e) {
        if (e.code === "Enter" && !e.shiftKey) {  // enter, return
            input.value = input.value.slice(0, -1); //Remove enter
            submitBtn.click();
        }
    };

    submitBtn.onclick = function(e) {
        if (!isInputEnabled)
            return;
        chatSocket.send(JSON.stringify({
            type: "command",
            payload: {
                action: "create_message",
                "chat_id": cur_chat,
                content: input.value
            }
        }));
        const message = {author: 1, content: input.value, id: -1};
        
        let chat = chats.find((c) => c.id === cur_chat);
        chat.enabled = false;
        chat.messages.push(message);
        chatDiv.appendChild(formMessage(message));
        input.value = '';
        setInputEnabled(false);
        input.oninput();
        scrollToEnd();
    };

    document.getElementById('chat-speak-message').addEventListener('click', (e) => {
        startVoiceInput();
    });

    document.getElementById('chats').addEventListener('click', (e) => {
        let target = e.target;

        if (!target.dataset.id)
            return;

        openChat(parseInt(target.dataset.id));
    });

    document.getElementById("create-chat-btn").addEventListener("click", createChat);


    document.querySelectorAll("textarea").forEach(function(textarea) {
        textarea.style.height = textarea.scrollHeight + "px";
        
        textarea.oninput = function() {
            this.style.height = "auto";
            this.style.height = Math.min(this.scrollHeight, 200) + "px";
        }
    });
});
