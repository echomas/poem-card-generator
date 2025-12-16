# 📜 Multi-Language Poem Card Generator

这是一个基于 Python 的自动化内容生产工具。它可以根据输入的诗歌标题和作者，自动调用 LLM (DeepSeek/GPT-4) 获取多语言版本（中、英、法、俄、德等），并进行人工校验，最终渲染成极具质感的复古风诗歌卡片。

![Cover](https://via.placeholder.com/800x400?text=Poem+Generator+Demo) 
*(建议后续在这里放一张你生成的精美样图)*

## ✨ 功能特性 (Features)

* **多语言自动获取**：自动检索诗歌的 6 种语言版本（含作者名本地化）。
* **Human-in-the-Loop**：支持“采集 -> 人工校验 -> 渲染”的断点续传工作流。
* **动态视觉渲染**：
    * 根据诗歌长度自动计算画布高度（支持长诗）。
    * 自动生成带玫瑰暗纹和噪点的复古信纸背景。
    * 内置排版引擎：支持动态字号、段落间距优化。
* **严谨的校验机制**：包含字体缺失检测、语言真实性检测。

## 🛠️ 安装与使用 (Usage)

### 1. 环境准备
```bash
git clone [https://github.com/你的用户名/poem-card-generator.git](https://github.com/你的用户名/poem-card-generator.git)
cd poem-card-generator
pip install -r requirements.txt
```
### 2. 配置密钥

复制 .env.example 为 .env，并填入你的 API Key：

```text
OPENAI_API_KEY=sk-xxxxxx
OPENAI_BASE_URL=[https://api.deepseek.com](https://api.deepseek.com)
```
### 3. 准备资源

请确保 `assets/fonts` 目录下包含以下字体文件（需自行下载）：
- `serif_cn.ttf` (推荐: 思源宋体 SC)
- `serif_tw.ttf` (推荐: 思源宋体 TC)
- `serif_latin.ttf` (推荐: Lora - 支持西文和俄文)

### 4. 运行

```Bash
python main.py
```
#### 按照终端提示选择模式：
- 输入 1: 采集数据并保存为 JSON。
- (人工修改 JSON 后)
- 输入 2: 读取 JSON 并批量生成图片。