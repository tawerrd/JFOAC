# Live2D Widget

![](https://forthebadge.com/images/badges/built-with-love.svg)
![](https://forthebadge.com/images/badges/uses-html.svg)
![](https://forthebadge.com/images/badges/made-with-javascript.svg)
![](https://forthebadge.com/images/badges/contains-cat-gifs.svg)
![](https://forthebadge.com/images/badges/powered-by-electricity.svg)
![](https://forthebadge.com/images/badges/makes-people-smile.svg)


# 原工程项目

[stevenjoezhang/live2d-widget](https://github.com/stevenjoezhang/live2d-widget)

## 特性

在网页中添加 Live2D 看板娘。兼容 PJAX，支持无刷新加载。

<img src="assets/screenshot-2.png" width="280"><img src="assets/screenshot-3.png" width="280"><img src="assets/screenshot-1.png" width="270">

（注：以上人物模型仅供展示之用，本仓库并不包含任何模型。）

你也可以查看示例网页：

- 在 [米米的博客](https://zhangshuqiao.org) 的左下角可查看效果
- [demo.html](https://mi.js.org/live2d-widget/demo/demo.html)，展现基础功能
- [login.html](https://mi.js.org/live2d-widget/demo/login.html)，仿 NPM 的登陆界面

## 使用

在 html 页面的 `head` 或 `body` 加载脚本
```xml
<script src="https://fastly.jsdelivr.net/gh/spite-triangle/live2d-widget@latest/autoload.js"></script>
```
添加代码的位置取决于你的网站的构建方式。例如，如果你使用的是 [Hexo](https://hexo.io)，那么需要在主题的模版文件中添加以上代码。对于用各种模版引擎生成的页面，修改方法类似。  
如果网站启用了 PJAX，由于看板娘不必每页刷新，需要注意将该脚本放到 PJAX 刷新区域之外。


## 配置

你可以对照 `autoload.js` 的源码查看可选的配置项目。`autoload.js` 会自动加载 `live2d-widget` 三个文件：`waifu.css`，`live2d.min.js` 和 `waifu-tips.js`。`waifu-tips.js` 会创建 `initWidget` 函数，这就是加载看板娘的主函数。`initWidget` 函数接收一个 Object 类型的参数，作为看板娘的配置。以下是配置选项：

| 选项        | 类型       | 默认值                                                                               | 说明                       |
| ----------- | ---------- | ------------------------------------------------------------------------------------ | -------------------------- |
| `waifuPath` | `string`   | `https://fastly.jsdelivr.net/gh/stevenjoezhang/live2d-widget@latest/waifu-tips.json` | 看板娘资源路径，可自行修改 |
| `apiPath`   | `string`   | `https://live2d.fghrsh.net/api/`                                                     | API 路径，可选参数         |
| `cdnPath`   | `string`   | `https://fastly.jsdelivr.net/gh/fghrsh/live2d_api/`                                  | CDN 路径，可选参数         |
| `tools`     | `string[]` | 见 `autoload.js`                                                                     | 加载的小工具按钮，可选参数 |

其中，`apiPath` 和 `cdnPath` 两个参数设置其中一项即可。`apiPath` 是后端 API 的 URL，可以自行搭建，并增加模型（需要修改的内容比较多，此处不再赘述），可以参考 [live2d_api](https://github.com/fghrsh/live2d_api)。而 `cdnPath` 则是通过 jsDelivr 这样的 CDN 服务加载资源，更加稳定。

## 自定义

如果以上「配置」部分提供的选项还不足以满足你的需求，那么你可以自己进行修改。本仓库的目录结构如下：

- `src/waifu-tips.js` 包含了按钮和对话框的逻辑；
- `live2d-widget/waifu-tips.js` 是由 `src/waifu-tips.js` 自动打包生成的，不建议直接修改；
- `live2d-widget/waifu-tips.json` 中定义了触发条件（`selector`，CSS 选择器）和触发时显示的文字（`text`）；
- `live2d-widget/waifu.css` 是看板娘的样式表。

> 自定义配置，只需 `git clone` 当前项目，然后修改 `live2d-widget` 下的配置或者重新编译 `waifu-tips.js`


`waifu-tips.json` 中默认的 CSS 选择器规则是对 Hexo 的 [NexT 主题](http://github.com/next-theme/hexo-theme-next) 有效的，为了适用于你自己的网页，可能需要自行修改，或增加新内容。  
**警告：`waifu-tips.json` 中的内容可能不适合所有年龄段，或不宜在工作期间访问。在使用时，请自行确保它们是合适的。**

要在本地部署本项目的开发测试环境，你需要安装 Node.js 和 npm，然后执行以下命令：

```bash
git clone https://github.com/spite-triangle/live2d-widget.git
npm install
npm run build
```
