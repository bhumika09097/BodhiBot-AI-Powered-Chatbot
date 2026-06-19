const inputField = document.querySelector(".input-section input");

const sendBtn = document.querySelector(".input-section button");

const chatContainer = document.querySelector(".chat-container");

const hero = document.querySelector(".hero-section");

document.getElementById("new-chat-btn").addEventListener("click", () => {
    window.location.href = "/new_chat";
});

document
  .getElementById("sidebar-new-chat-btn")
  .addEventListener("click", () => {
    window.location.href = "/new_chat";
});

sendBtn.addEventListener("click", () => {
    hero.style.display = "none";
});

/* SEND MESSAGE */

async function sendMessage(){

    const message = inputField.value.trim();

    if(message === ""){
        return;
    }

    /* USER MESSAGE */

    appendMessage(message, "user-message");

    inputField.value = "";

    scrollToBottom();

    /* BOT TYPING */

    const typingDiv = appendMessage("Typing...", "bot-message");

    try{

        const response = await fetch("/chat",{

            method: "POST",

            headers:{
                "Content-Type":"application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        typingDiv.textContent = "";

        typeEffect(typingDiv, data.reply);

    }
    catch(error){

        typingDiv.textContent = "Something went wrong.";
    }
}

/* APPEND MESSAGE */

function appendMessage(text, className){

    const div = document.createElement("div");

    div.classList.add(className);

    div.textContent = text;

    chatContainer.appendChild(div);

    return div;
}

/* TYPING EFFECT */

function typeEffect(element, text){

    let index = 0;

    const interval = setInterval(() => {

        if(index < text.length){

            element.textContent += text.charAt(index);

            index++;

            scrollToBottom();
        }
        else{
            clearInterval(interval);
        }

    }, 20);
}

/* AUTO SCROLL */

function scrollToBottom(){

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/* ENTER KEY */

inputField.addEventListener("keypress",(e)=>{

    if(e.key === "Enter"){
        sendMessage();
    }
});

/* SEND BUTTON */

sendBtn.addEventListener("click", sendMessage);

async function loadConversations(){

    const response = await fetch("/conversations");

    const conversations = await response.json();

    const container = document.getElementById("conversation-list");

    container.innerHTML = "";

    conversations.forEach(chat => {

        const div = document.createElement("div");

        div.textContent = chat.title || `Chat ${chat.id}`;

        div.classList.add("chat-item");

        div.addEventListener("click", () => {
            openConversation(chat.id);
        });

        container.appendChild(div);
    });
}

loadConversations();

async function openConversation(conversationId){

    await fetch(`/set_conversation/${conversationId}`);
    
    const response = await fetch(
        `/conversation/${conversationId}`
    );

    const messages = await response.json();

    chatContainer.innerHTML = "";

    hero.style.display = "none";

    messages.forEach(msg => {

        if(msg.role === "user"){
            appendMessage(msg.content, "user-message");
        }
        else{
            appendMessage(msg.content, "bot-message");
        }
    });

    scrollToBottom();
}
