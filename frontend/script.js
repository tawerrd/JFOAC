const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
 const data = JSON.parse(event.data);
 if (data.type === 'message') {
 addChatMessage('ai', data.message);
 } else if (data.type === 'emotion') {
 setLive2DEmotion(data.emotion);
 }
};

function addChatMessage(sender, message) {
 const chatContainer = document.getElementById('chat-container');
 const messageDiv = document.createElement('div');
 messageDiv.classList.add('chat-message', sender);
 messageDiv.textContent = message;
 chatContainer.appendChild(messageDiv);
 chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Placeholder for setting Live2D emotion
function setLive2DEmotion(emotion) {
 // For spite-triangle/live2d-widget, you may need to implement this based on the library's API
 console.log('Set emotion to', emotion);
}

const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(e) {
 if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
 const message = userInput.value.trim();
 if (message) {
 addChatMessage('user', message);
 ws.send(JSON.stringify({ type: 'message', content: message }));
 userInput.value = '';
 }
}