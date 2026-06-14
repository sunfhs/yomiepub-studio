# YomiEpub Studio

简体中文 | [English](README.md)

<p align="center">
  <img src="docs/assets/yomiepub-studio-icon.png" alt="YomiEpub Studio 图标" width="112">
</p>

YomiEpub Studio 是一个本地网页小工具，用来把日文 EPUB/TXT/HTML 转成更适合 KOReader 阅读的 EPUB：横排、带ふりがな、适配安卓电纸书。

它主要面向中国大陆安卓电纸书用户，比如汉王、文石国行、掌阅系设备，尤其是自带阅读器对日文竖排、ruby 注音、复杂 EPUB CSS 支持不稳定的情况。

<p align="center">
  <img src="docs/assets/yomiepub-studio-home.png" alt="YomiEpub Studio 本地网页界面" width="900">
</p>

## 它能做什么

- 把本地日文 EPUB/TXT/HTML 转成横排 EPUB。
- 给日文汉字添加ふりがな，使用标准 HTML ruby 标签。
- 重新打包 EPUB，让它更适合 KOReader 打开。
- 转换时显示进度条，完成后自动下载 `Yomi.epub` 文件。
- 在本机运行：`http://127.0.0.1:8765`。
- 文件只在你的电脑里处理，不上传云端。

生成的 ruby 大概长这样：

```html
<ruby>日本語<rt>にほんご</rt></ruby>
```

## 它不做什么

本项目不提供电子书下载、盗版搜索、Z-Library 自动化、DRM 解除，也不提供任何版权内容访问。

请只处理你自己合法获得、拥有使用权的本地电子书文件。

仓库里的截图尽量避免使用受版权保护的书页。如果你要补充截图，建议使用软件界面截图或公版文本。

## 推荐阅读方案

- 日文小说、需要ふりがな或自定义排版：推荐 KOReader。
- 中文/英文普通阅读：微信读书或设备自带阅读器可能就够了。

KOReader 支持 Android，也支持 EPUB、PDF、MOBI、TXT、HTML、RTF、CHM 等格式。

- KOReader 官网：https://koreader.rocks/
- KOReader GitHub Releases：https://github.com/koreader/koreader/releases

## 快速开始

### 下载

- 项目 Release：https://github.com/sunfhs/yomiepub-studio/releases/latest
- 源码 ZIP：在 GitHub 页面点击 **Code -> Download ZIP**。
- Release 页面里附带了一个 KOReader Android APK，方便测试；如果你想要最新官方版本，请优先从 KOReader 官网或官方 GitHub Releases 下载。

### 最简单方式：macOS App 启动

从 GitHub 下载 ZIP，解压后进入项目文件夹：

- macOS：双击 `YomiEpub Studio.app`
- Windows：双击 `start_yomiepub.bat`

前提：电脑需要安装 Python 3.10 或更新版本。没有的话，从这里安装：

https://www.python.org/downloads/

macOS App 会自动做这些事：

1. 在 `~/Library/Application Support/YomiEpub Studio/venv` 创建本地 Python 环境
2. 安装 App 自带的 YomiEpub Studio wheel 包
3. 启动本地网页服务
4. 自动打开 `http://127.0.0.1:8765`

第一次启动需要联网，因为 Python 依赖会从 PyPI 安装。之后再次启动会快很多。

如果 macOS 提示“无法打开，因为来自未知开发者”：

1. 右键点击 `YomiEpub Studio.app`
2. 选择 **打开**
3. 再确认一次 **打开**

如果浏览器没有自动弹到前台，手动打开这个地址即可：

```text
http://127.0.0.1:8765
```

macOS 备用方式：双击 `start_yomiepub.command`。这个方式会打开 Terminal 窗口，并把本地服务挂在这个窗口上。

## 网页使用流程

1. 打开 `http://127.0.0.1:8765`。
2. 选择你本地已有的合法日文 EPUB/TXT/HTML 文件。
3. 点击 **Convert & Download EPUB**。
4. 等待进度条完成。
5. 下载生成的 `书名Yomi.epub`。
6. 通过 Wi-Fi 传书、USB、Syncthing 等方式传到电纸书。
7. 用 KOReader 打开阅读。

## 命令行安装

如果你熟悉命令行，也可以这样安装：

```bash
git clone https://github.com/sunfhs/yomiepub-studio.git
cd yomiepub-studio
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

启动本地网页：

```bash
jp-ebook-web
```

然后浏览器打开：

```text
http://127.0.0.1:8765
```

命令行转换：

```bash
jp-ebook-convert input.epub --furigana --horizontal --output output.epub
```

运行测试：

```bash
pytest
```

## 命令行参数

```bash
jp-ebook-convert INPUT --output OUTPUT [--furigana] [--horizontal] [--font-size 1.05em] [--line-height 1.9]
```

常用参数：

- `--furigana`：给日文汉字添加 ruby 注音
- `--horizontal`：强制横排
- `--font-size`：生成内容的字号
- `--line-height`：行距，适合电纸书阅读
- `--bilingual`：预留给未来双语版本，目前未实现

## 当前功能范围

已经实现：

- 本地 FastAPI 网页界面
- macOS `.app` 启动器
- macOS / Windows 备用双击启动器
- EPUB/TXT/HTML 输入
- 横排排版清理
- 使用 `pykakasi` 添加ふりがな
- KOReader 友好的 EPUB 重新打包
- 转换进度条
- 本地处理，不上传云端
- 核心转换逻辑测试

未来可以继续做：

- 中日双语逐段对照
- 用户自行配置翻译后端
- 按 JLPT 或难词程度控制注音范围
- 更完整的桌面应用打包

## 项目结构

```text
yomiepub-studio/
├── README.md
├── README.zh-CN.md
├── docs/
│   └── assets/
├── app/
│   ├── backend/
│   └── frontend/
├── samples/
├── scripts/
├── tests/
├── YomiEpub Studio.app/
├── start_yomiepub.command
├── start_yomiepub.bat
├── pyproject.toml
└── LICENSE
```

## 电纸书使用 SOP

1. 从 KOReader 官网或 GitHub Releases 安装 Android APK。
2. 用 YomiEpub Studio 转换本地日文电子书。
3. 把生成的 EPUB 通过 Wi-Fi 传书、USB、Syncthing 等方式传到电纸书。
4. 在 KOReader 里把根目录设置到传书目录。
5. 打开转换后的 EPUB 阅读。

## 许可证

MIT

## 法律与使用边界

YomiEpub Studio 是一个本地格式转换和阅读辅助工具，适合学习、无障碍阅读和个人阅读流程。

请不要用它分发版权内容、绕过 DRM、爬取盗版网站，或自动化下载未授权电子书。
