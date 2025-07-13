from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import os
from openai import OpenAI
import asyncio
from datetime import datetime, timedelta

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL", "[invalid url, do not cite])
client = OpenAI(base_url=openai_base_url, api_key=openai_api_key)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    system_prompt = {"role": "system", "content": "You are a helpful assistant. For each of your responses, please also indicate your current emotion from the following list: crying, smiling, laughing, sad, neutral, based on the content of your response, and include it at the end in the format [emotion: xxx]."}
    conversation = [system_prompt]
    last_activity = datetime.now()

    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=3)
                user_message = {"role": "user", "content": data}
                conversation.append(user_message)
                response = client.chat.completions.create(model="gpt-3.5-turbo", messages=conversation, max_tokens=100, temperature=0.7)
                ai_message = response.choices[0].message.content
                if "[emotion:" in ai_message:
                    parts = ai_message.rsplit("[emotion:", 1)
                    if len(parts) > 1:
                        emotion_part = parts[1].split("]")[0].strip()
                        ai_message = parts[0].strip()
                    else:
                        emotion_part = "neutral"
                else:
                    emotion_part = "neutral"
                conversation.append({"role": "assistant", "content": ai_message})
                await websocket.send_text(f"message:{ai_message}")
                await websocket.send_text(f"emotion:{emotion_part}")
                last_activity = datetime.now()
            except asyncio.TimeoutError:
                now = datetime.now()
                if (now - last_activity) > timedelta(seconds=3):
                    system_inactivity_message = {"role": "user", "content": "(sys:用户3秒未发送任何东西)"}
                    conversation.append(system_inactivity_message)
                    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=conversation, max_tokens=100, temperature=0.7)
                    ai_message = response.choices[0].message.content
                    if "[emotion:" in ai_message:
                        parts = ai_message.rsplit("[emotion:", 1)
                        if len(parts) > 1:
                            emotion_part = parts[1].split("]")[0].strip()
                            ai_message = parts[0].strip()
                        else:
                            emotion_part = "neutral"
                    else:
                        emotion_part = "neutral"
                    conversation.append({"role": "assistant", "content": ai_message})
                    await websocket.send_text(f"message:{ai_message}")
                    await websocket.send_text(f"emotion:{emotion_part}")
                    last_activity = now
    except WebSocketDisconnect:
        print("WebSocket disconnected")
