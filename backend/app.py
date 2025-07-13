from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import os
from openai import OpenAI
import asyncio
from datetime import datetime, timedelta
import json

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Load API config from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL", "[invalid url, do not cite])
client = OpenAI(base_url=openai_base_url, api_key=openai_api_key)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
 await websocket.accept()
 conversation = [
 {"role": "system", "content": "You are a helpful assistant. For each of your responses, please also indicate your current emotion from the following list: crying, smiling, laughing, sad, neutral, based on the content of your response, and include it at the end in the format [emotion: xxx]."}
 ]
 last_user_message_time = None

 async def inactivity_checker():
 while True:
 await asyncio.sleep(3)
 current_time = datetime.now()
 if last_user_message_time is None or (current_time - last_user_message_time) > timedelta(seconds=3):
 # Send system message
 system_message = {"role": "user", "content": "(sys:用户3秒未发送任何东西)"}
 conversation.append(system_message)
 response = client.chat.completions.create(
 model="gpt-3.5-turbo",
 messages=conversation,
 max_tokens=100,
 temperature=0.7
 )
 ai_message = response.choices[0].message.content
 # Parse emotion
 emotion = "neutral"
 if "[emotion:" in ai_message:
 parts = ai_message.rsplit("[emotion:", 1)
 if len(parts) > 1:
 emotion = parts[1].split("]")[0].strip()
 ai_message = parts[0].strip()
 conversation.append({"role": "assistant", "content": ai_message})
 await websocket.send_text(json.dumps({"type": "message", "message": ai_message}))
 await websocket.send_text(json.dumps({"type": "emotion", "emotion": emotion}))

 # Start the inactivity checker
 checker_task = asyncio.create_task(inactivity_checker())

 try:
 while True:
 data = await websocket.receive_text()
 message_data = json.loads(data)
 if message_data["type"] == "message":
 user_message = {"role": "user", "content": message_data["content"]}
 conversation.append(user_message)
 last_user_message_time = datetime.now()
 response = client.chat.completions.create(
 model="gpt-3.5-turbo",
 messages=conversation,
 max_tokens=100,
 temperature=0.7
 )
 ai_message = response.choices[0].message.content
 # Parse emotion
 emotion = "neutral"
 if "[emotion:" in ai_message:
 parts = ai_message.rsplit("[emotion:", 1)
 if len(parts) > 1:
 emotion = parts[1].split("]")[0].strip()
 ai_message = parts[0].strip()
 conversation.append({"role": "assistant", "content": ai_message})
 await websocket.send_text(json.dumps({"type": "message", "message": ai_message}))
 await websocket.send_text(json.dumps({"type": "emotion", "emotion": emotion}))
 except WebSocketDisconnect:
 checker_task.cancel()
 print("WebSocket disconnected")
