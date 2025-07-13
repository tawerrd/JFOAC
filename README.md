## A chat front-end that combines Live2d and Openai

### What is it?
This is a front-end extension that combines Live2D and OpenAI, enabling OpenAI character role-playing to work with Live2D, allowing Live2D to create corresponding expressions,In addition, I also added a time system that allows the AI to have a sense of time, for example, it has been n seconds since you last chatted with the AI, and at the same time, let the chat area show the thoughts of the AI waiting for you to chat.

### Based on
This project is developed using Python/HTML/CSS/JS

### Secondary development and usage

Built-in Live2D module call

```html
<script src="https://raw.githubusercontent.com/tawerrd/JFOAC/refs/heads/main/static/live2d-widget/autoload.js"></script>
```

Dependent installation

```html
pip install -r requirements.txt
```
Upload a Live2D model
```html
\static\live2d\models\yourmodel
```
Modify the model configuration
```html
index.html→ modelUrl: '/static/live2d/models/modelname',
```
Modify the API address and key
```html
app.py→ openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL", "[invalid url, do not cite])
```
run
```html
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```
### visit
http://127.0.0.1:8000

### combine
You can combine this frontend with wordpress/typecho/hexo, etc

Usually added:
```html
<iframe src="http://127.0.0.1:8000" width="100%" height="80" scrolling="no"frameborder="no"></iframe>
```
Or develop and use a separate interface yourself

![:name](https://count.getloli.com/@JFOCsadsfhuiasjdnih?name=JFOCsadsfhuiasjdnih&theme=kasuterura-4&padding=9&offset=0&align=top&scale=1&pixelated=0&darkmode=0)

