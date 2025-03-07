document.addEventListener("DOMContentLoaded", function () {
    const ws = new WebSocket("ws://localhost:8000/chatbot");
    const messageInput = document.getElementById("messageText");
    const sendButton = document.getElementById("sendButton");
    const messagesContainer = document.getElementById("messages");

    ws.onmessage = function (event) {
        appendMessage("bot", event.data);
    };

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message === "") return;

        appendMessage("user", message);
        ws.send(message);
        messageInput.value = "";
    }

    function appendMessage(sender, message) {
        const msgElement = document.createElement("div");
        msgElement.textContent = message;
        msgElement.classList.add("message", sender === "user" ? "user-message" : "bot-message");

        messagesContainer.appendChild(msgElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll to latest message
    }

    // Send message on button click
    sendButton.addEventListener("click", sendMessage);

    // Send message when pressing "Enter"
    messageInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent new line in input field
            sendMessage();
        }
    });
});
