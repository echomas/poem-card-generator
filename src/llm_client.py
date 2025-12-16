import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url if base_url else None)

MODEL_NAME = "deepseek-chat"  # 或 gpt-4-turbo

# === 核心修改：要求 JSON 包含 author 字段 ===
SYSTEM_PROMPT = """
你是一个精通多国语言的资深诗歌编辑。请根据用户提供的【诗名+作者】，检索该诗歌的 6 个语言版本。

核心要求：
1. **全链路本地化**：不仅标题和内容要翻译，**作者名也必须翻译成对应语言**。
   - 法文版作者必须是法文写法（如 "Alexandre Pouchkine"）。
   - 俄文版作者必须是俄文写法（如 "Александр Пушкин"）。
   - 繁体中文版作者名请使用繁体字（如 "普希金"）。
2. **准确性优先**：检索权威原文。
3. **格式整洁**：Content（正文）中只保留诗句，不要带标题。

强制 JSON 输出格式：
{
    "zh_cn": {
        "title": "中文简体标题",
        "author": "中文简体作者名",
        "content": "内容..."
    },
    "zh_tw": {
        "title": "中文繁體標題",
        "author": "中文繁體作者名",
        "content": "內容..."
    },
    "en": {
        "title": "English Title",
        "author": "English Author Name",
        "content": "Content..."
    },
    "fr": {
        "title": "Titre Français",
        "author": "Auteur Français",
        "content": "Contenu..."
    },
    "de": {
        "title": "Deutscher Titel",
        "author": "Deutscher Autor",
        "content": "Inhalt..."
    },
    "ru": {
        "title": "Русское Название",
        "author": "Русский Автор",
        "content": "Содержание..."
    },
    "xhs_copy": "小红书文案..."
}
"""


def fetch_poem_data_v2(title, author):
    # 提示词微调，强调作者名翻译
    prompt = f"请处理诗歌：《{title}》，作者：{author}。请确保输出所有 6 种语言的【标题】、【作者名】和【正文】。"
    print(f"🤖 正在调用 AI 检索多语言数据 (含作者名本地化)...")

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return {}

# 测试代码（仅在直接运行此文件时执行）
if __name__ == "__main__":
    test_data = fetch_poem_data_v2("哀歌", "普希金")
    print(json.dumps(test_data, ensure_ascii=False, indent=2))