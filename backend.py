from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO
import time
import openai

app = Flask(__name__)
socketio = SocketIO(app)

openai.api_key = "YOUR_OPENAI_API_KEY"

messages = {}
last_user_message_times = {}
last_automatic_sent_times = {}

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    messages[sid] = [
        {"role": "system", "content": "You are a friendly AI assistant. For each response, first provide your answer to the user's query. Then, on a new line, provide a single word that describes your current emotion based on your response, considering your role as a friendly AI assistant. Format it as 'Emotion: [emotion]'."}
    ]
    last_user_message_times[sid] = time.time()
    last_automatic_sent_times[sid] = None

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in messages: del messages[sid]
    if sid in last_user_message_times: del last_user_message_times[sid]
    if sid in last_automatic_sent_times: del last_automatic_sent_times[sid]

@socketio.on('message')
def handle_message(data):
    sid = request.sid
    user_message = data['content']
    messages[sid].append({"role": "user", "content": user_message})
    last_user_message_times[sid] = time.time()
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages[sid])
    ai_response = response['choices'][0]['message']['content']
    lines = ai_response.split('\n')
    text = '\n'.join(lines[:-1])
    emotion = lines[-1].split(':')[1].strip() if lines[-1].startswith('Emotion: ') else "neutral"
    image_response = openai.Image.create(prompt=f"A {emotion} face of a friendly AI assistant", n=1, size="256x256")
    image_url = image_response['data'][0]['url']
    socketio.emit('response', {'content': text, 'image_url': image_url}, room=sid)
    messages[sid].append({"role": "assistant", "content": text})

def check_inactivity():
    while True:
        socketio.sleep(1)
        current_time = time.time()
        for sid in list(last_user_message_times.keys()):
            if current_time - last_user_message_times[sid] > 3 and (last_automatic_sent_times.get(sid) is None or current_time - last_automatic_sent_times[sid] > 3):
                temp_messages = messages[sid].copy()
                temp_messages.append({"role": "system", "content": "The user has not sent any message for 3 seconds."})
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=temp_messages)
                ai_response = response['choices'][0]['message']['content']
                lines = ai_response.split('\n')
                text = '\n'.join(lines[:-1])
                emotion = lines[-1].split(':')[1].strip() if lines[-1].startswith('Emotion: ') else "neutral"
                image_response = openai.Image.create(prompt=f"A {emotion} face of a friendly AI assistant", n=1, size="256x256")
                image_url = image_response['data'][0]['url']
                socketio.emit('response', {'content': text, 'image_url': image_url}, room=sid)
                last_automatic_sent_times[sid] = current_time
                messages[sid].append({"role": "assistant", "content": text})

socketio.start_background_task(check_inactivity)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
