L2Dwidget.init({
    'model': {'jsonPath': '/static/live2d/model/model.json'},
    'display': {
        'position': 'fixed',
        'width': 200,
        'height': 400,
        'top': '10px',
        'left': '50%',
        'transform': 'translateX(-50%)'
    },
    'mobile': {'show': true}
});

const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
    const data = event.data;
    if (data.startsWith('message:')) {
        const message = data.split('message:')[1];
        addChatMessage('ai', message);
    } else if (data.startsWith('emotion:')) {
        const emotion = data.split('emotion:')[1];
        setLive2DEmotion(emotion);
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

function setLive2DEmotion(emotion) {
    const expressionMap = {
        'crying': 'crying',
        'smiling': 'smiling',
        'laughing': 'laughing',
        'sad': 'sad',
        'neutral': 'normal'
    };
    const expr = expressionMap[emotion] || 'normal';
    L2Dwidget.setExpression(expr);
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
        ws.send(message);
        userInput.value = '';
    }
}
