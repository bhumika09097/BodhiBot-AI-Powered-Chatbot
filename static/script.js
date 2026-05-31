const inputField = document.querySelector(".input-section input");

const sendBtn = document.querySelector(".input-section button");

const chatContainer = document.querySelector(".chat-container");

const hero = document.querySelector(".hero-section");


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