## 一个结合了Live2d和Openai的聊天前端

### 这是什么?
这是一个结合了Live2d和openai的前端扩展,让openai角色扮演可以配套live2d,使live2d可以做出相应表情,另外我还添加的时间系统,可以让ai拥有时间观念,比如你距离上次找ai聊天已经过去了n秒,同时让聊天区显示ai等待你聊天时的思考。

### 基于
本项目基于python/html/css/js开发

### 二次开发及使用

内置live2d模块调用

```html
<script src="https://raw.githubusercontent.com/tawerrd/JFOAC/refs/heads/main/static/live2d-widget/autoload.js"></script>
```

依赖安装

```html
pip install -r requirements.txt
```
上传live2d模型
```html
\static\live2d\models\yourmodel
```
修改model配置
```html
index.html→ modelUrl: '/static/live2d/models/modelname',
```
修改api地址和key
```html
app.py→ openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL", "[invalid url, do not cite])
```
运行
```html
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```
### 访问
http://127.0.0.1:8000

### 结合
你可以将此前端结合于wordpress/typecho/hexo等

通常添加:
```html
<iframe src="http://127.0.0.1:8000" width="100%" height="80" scrolling="no"frameborder="no"></iframe>
```
或者自行开发和使用单独界面

![:name](https://count.getloli.com/@JFOCsadsfhuiasjdnih?name=JFOCsadsfhuiasjdnih&theme=kasuterura-4&padding=9&offset=0&align=top&scale=1&pixelated=0&darkmode=0)
