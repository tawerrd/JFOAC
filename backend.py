from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import time

app = Flask(__name__)
socketio = SocketIO(app)

# API 配置（可自定义）
api_base = "[invalid url, do not cite]
api_key = "YOUR_API_KEY"  # 替换为您的 API Key
headers = {"Authorization": f"Bearer {api_key}"}

# 系统消息（定义 AI 的角色和行为）
system_message = {
    "role": "system",
    "content": "You will play as Ella, the Ella of Plastic Memories. For each response, start by providing an answer to the user's query. Then, on the new line, give a word to describe your current mood based on your response, considering your role as Ella. Format it as 'emotion: [emotion]"."
}

# 每个用户的状态
messages = {}
last_message_times = {}
has_sent_automatic = {}

# 连接事件
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    messages[sid] = [system_message.copy()]
    last_message_times[sid] = time.time()
    has_sent_automatic[sid] = False

# 断开连接事件
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in messages:
        del messages[sid]
    if sid in last_message_times:
        del last_message_times[sid]
    if sid in has_sent_automatic:
        del has_sent_automatic[sid]

# 用户发送消息事件
@socketio.on('send_message')
def handle_send_message(data):
    sid = request.sid
    user_message = data['content']
    messages[sid].append({"role": "user", "content": user_message})
    last_message_times[sid] = time.time()
    has_sent_automatic[sid] = False
    # 将用户消息发送到客户端
    socketio.emit('new_message', {'type': 'user', 'content': user_message}, room=sid)
    # 获取 AI 回复
    response = get_chat_completion(messages[sid])
    ai_content = response['choices'][0]['message']['content']
    # 解析情绪
    lines = ai_content.split('\n')
    if len(lines) >= 2 and lines[-1].startswith('Emotion: '):
        emotion = lines[-1].split('Emotion: ')[1].strip()
        ai_text = '\n'.join(lines[:-1])
    else:
        emotion = "neutral"
        ai_text = ai_content
    # 生成表情图片
    image_prompt = f"A {emotion} face of a friendly AI assistant"
    image_response = generate_image(image_prompt)
    image_url = image_response['data'][0]['url']
    # 将 AI 回复和图片发送到客户端
    socketio.emit('new_message', {'type': 'ai', 'content': ai_text, 'image_url': image_url}, room=sid)
    # 添加 AI 回复到消息历史
    messages[sid].append({"role": "assistant", "content": ai_text})

# 调用聊天 API
def get_chat_completion(messages_list):
    url = f"{api_base}/chat/completions"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages_list
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 调用图片生成 API
def generate_image(prompt):
    url = f"{api_base}/images/generations"
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "256x256"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 检查用户是否超时（3 秒无活动）
def check_inactivity():
    while True:
        socketio.sleep(1)
        current_time = time.time()
        for sid in list(last_message_times.keys()):
            if current_time - last_message_times[sid] > 3 and not has_sent_automatic[sid]:
                automatic_msg = "(sys:用户3秒未发送任何东西)"
                # 添加自动消息到消息历史
                messages[sid].append({"role": "user", "content": automatic_msg})
                # 将自动消息发送到客户端
                socketio.emit('new_message', {'type': 'user', 'content': automatic_msg}, room=sid)
                # 获取 AI 回复
                response = get_chat_completion(messages[sid])
                ai_content = response['choices'][0]['message']['content']
                # 解析情绪
                lines = ai_content.split('\n')
                if len(lines) >= 2 and lines[-1].startswith('Emotion: '):
                    emotion = lines[-1].split('Emotion: ')[1].strip()
                    ai_text = '\n'.join(lines[:-1])
                else:
                    emotion = "neutral"
                    ai_text = ai_content
                # 生成表情图片
                image_prompt = f"A {emotion} face of a friendly AI assistant"
                image_response = generate_image(image_prompt)
                image_url = image_response['data'][0]['url']
                # 将 AI 回复和图片发送到客户端
                socketio.emit('new_message', {'type': 'ai', 'content': ai_text, 'image_url': image_url}, room=sid)
                # 添加 AI 回复到消息历史
                messages[sid].append({"role": "assistant", "content": ai_text})
                # 设置自动消息已发送标志
                has_sent_automatic[sid] = True

# 启动后台任务检查超时
socketio.start_background_task(check_inactivity)

# 服务前端页面
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
