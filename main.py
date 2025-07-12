import gradio as gr
import openai
import time

openai.api_key = "YOUR_API_KEY"

system_message = {
    "role": "system",
    "content": "You are a friendly AI assistant. For each response, first provide your answer to the user's query. Then, on a new line, provide a single word that describes your current emotion based on your response, considering your role as a friendly AI assistant. Format it as 'Emotion: [emotion]'."
}

def get_display_messages(messages):
    display_messages = []
    for i in range(0, len(messages), 2):
        if i+1 < len(messages):
            user_msg = messages[i]['content']
            ai_msg = messages[i+1]['content']
            display_messages.append([user_msg, ai_msg])
    return display_messages

def get_ai_response(full_messages):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=full_messages
    )
    ai_response = completion.choices[0].message.content
    
    lines = ai_response.split('\n')
    emotion = "neutral"
    if len(lines) >= 2 and lines[-1].startswith('Emotion: '):
        emotion = lines[-1].split('Emotion: ')[1].strip()
        ai_response = '\n'.join(lines[:-1])
    
    image_response = openai.Image.create(
        prompt=f"A {emotion} face of a friendly AI assistant",
        n=1,
        size="256x256"
    )
    image_url = image_response['data'][0]['url']
    
    final_ai_response = f"{ai_response}<br>< img src='{image_url}' style='max-width:256px;'>"
    return final_ai_response

def user_message_fn(user_input, state):
    now = time.time()
    state['messages'].append({"role": "user", "content": user_input})
    state['last_user_time'] = now
    state['auto_sent'] = False
    
    full_messages = [system_message] + state['messages']
    ai_response = get_ai_response(full_messages)
    state['messages'].append({"role": "assistant", "content": ai_response})
    
    return get_display_messages(state['messages']), state, ""

def timer_fn(state):
    now = time.time()
    if state['last_user_time'] is not None and now - state['last_user_time'] > 3 and not state['auto_sent']:
        state['auto_sent'] = True
        auto_user_msg = "(sys:用户3秒未发送任何东西)"
        state['messages'].append({"role": "user", "content": auto_user_msg})
        
        full_messages = [system_message] + state['messages']
        ai_response = get_ai_response(full_messages)
        state['messages'].append({"role": "assistant", "content": ai_response})
    
    return get_display_messages(state['messages']), state

with gr.Blocks() as demo:
    state = gr.State(value={
        'messages': [],
        'last_user_time': None,
        'auto_sent': False
    })
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your Message")
    
    with gr.Row():
        submit = gr.Button("Send")
    
    timer = gr.Timer(value=1)
    
    submit.click(user_message_fn, inputs=[msg, state], outputs=[chatbot, state, msg])
    
    def clear_msg():
        return gr.update(value="")
    
    submit.click(clear_msg, outputs=msg)
    
    timer.tick(timer_fn, inputs=state, outputs=[chatbot, state])

demo.launch()
