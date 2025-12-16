import os
import json
import sys
from src.llm_client import fetch_poem_data_v2
from src.renderer import DynamicRenderer
from content_data import POEM_DATA_SOURCE

# === 配置 ===
# 中间文件存放位置
REVIEW_FILE = "poems_to_review.json"

# 字体配置 (保持不变)
FONT_CONFIG = {
    "zh_cn": "./assets/fonts/serif_cn.ttf",
    "zh_tw": "./assets/fonts/serif_tw.ttf",
    "en": "./assets/fonts/serif_latin.ttf",
    "fr": "./assets/fonts/serif_latin.ttf",
    "de": "./assets/fonts/serif_latin.ttf",
    "ru": "./assets/fonts/serif_latin.ttf"
}


def step_1_fetch_and_save():
    """
    第一步：只负责找 AI 要数据，存入 JSON，不画图。
    """
    print("\n🚀 进入【阶段一：数据采集】...")
    print(f"📋 计划处理 {len(POEM_DATA_SOURCE)} 首诗歌")

    collected_data = []

    for index, item in enumerate(POEM_DATA_SOURCE):
        title = item['title']
        author = item['author']
        print(f"\n[{index + 1}/{len(POEM_DATA_SOURCE)}] 正在请求 AI 获取: {title} - {author} ...")

        try:
            # 调用 LLM
            data = fetch_poem_data_v2(title, author)

            # 这是一个关键步骤：把原始的输入信息也记下来，方便生成文件夹名
            # 我们把 data 包装一下
            record = {
                "input_info": {"title": title, "author": author},
                "versions": data  # 这里面包含了 6 种语言的详细内容
            }
            collected_data.append(record)
            print("✅ 获取成功，已暂存。")

        except Exception as e:
            print(f"❌ 获取失败: {title}. 错误: {e}")

    # 保存到本地文件供人工校验
    with open(REVIEW_FILE, 'w', encoding='utf-8') as f:
        json.dump(collected_data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 数据已保存至: {REVIEW_FILE}")
    print("🛑 流程暂停。请打开该 JSON 文件进行人工校对，确认无误后运行第二步。")


def step_2_render_from_file():
    """
    第二步：读取本地 JSON (可能被人工改过)，批量生成图片。
    """
    print("\n🎨 进入【阶段二：视觉渲染】...")

    if not os.path.exists(REVIEW_FILE):
        print(f"❌ 找不到校验文件: {REVIEW_FILE}")
        print("请先运行第一步生成数据。")
        return

    # 读取校验后的数据
    with open(REVIEW_FILE, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    print(f"📂 读取到 {len(tasks)} 个任务，开始渲染...")

    renderer = DynamicRenderer()

    for task in tasks:
        # 解包数据
        input_info = task['input_info']
        versions = task['versions']  # 这是那 6 个语言的字典

        title_str = input_info['title']
        print(f"\nProcessing: {title_str}...")

        # 创建输出目录
        safe_title = title_str.replace(" ", "_")
        output_dir = f"./output/{safe_title}_多语言组图"
        os.makedirs(output_dir, exist_ok=True)

        # 保存文案 (如果有)
        if "xhs_copy" in versions:
            with open(f"{output_dir}/小红书文案.txt", 'w', encoding='utf-8') as f:
                f.write(versions["xhs_copy"])

        # 遍历语言生成图片
        # 过滤掉非语言的字段 (如 input_info, xhs_copy)
        valid_langs = [k for k in versions.keys() if k in FONT_CONFIG]

        for lang_code in valid_langs:
            lang_data = versions[lang_code]

            # 获取内容 (如果人工在JSON里改了，这里读到的就是改过的)
            poem_title = lang_data.get('title', 'Unknown')
            poem_author = lang_data.get('author', 'Unknown')
            poem_content = lang_data.get('content', '')

            render_data = {
                "title": poem_title,
                "author": poem_author,
                "content": poem_content
            }

            output_path = f"{output_dir}/{lang_code}.jpg"
            font_path = FONT_CONFIG[lang_code]

            renderer.render(
                data=render_data,
                font_path=font_path,
                output_path=output_path,
                font_size=40
            )

    print("\n✨ 全部渲染完成！请查看 output 目录。")


def main():
    while True:
        print("\n" + "=" * 30)
        print("   诗歌卡片生成器工作流 v3.0")
        print("=" * 30)
        print("1. [采集] 获取数据 -> 存为 poems_to_review.json")
        print("2. [渲染] 读取 JSON -> 生成最终图片")
        print("0. 退出")

        choice = input("\n请选择模式 (输入数字): ")

        if choice == "1":
            step_1_fetch_and_save()
            break  # 执行完一步就退出，强迫你去检查文件
        elif choice == "2":
            step_2_render_from_file()
            break
        elif choice == "0":
            sys.exit()
        else:
            print("输入无效，请重试。")


if __name__ == "__main__":
    main()

# import os
# import json
# from src.llm_client import fetch_poem_data_v2
#
# from src.renderer import DynamicRenderer
# from content_data import POEM_DATA_SOURCE
#
# # === 配置区域 ===
# TEMPLATE_PATH = "./assets/templates/paper_rose_texture.jpg"  # 确保是竖版 3:4
#
# # 字体映射配置：将语言代码映射到具体的字体文件
# # 确保你 assets/fonts/ 下有这些文件！
# FONT_CONFIG = {
#     "zh_cn": "./assets/fonts/serif_cn.ttf",  # 简体手写
#     "zh_tw": "./assets/fonts/serif_tw.ttf",  # 繁体手写
#     "en": "./assets/fonts/serif_latin.ttf",  # 英文手写
#     "fr": "./assets/fonts/serif_latin.ttf",  # 法文同上
#     "de": "./assets/fonts/serif_latin.ttf",  # 德文同上
#     "ru": "./assets/fonts/serif_latin.ttf"  # 俄文手写(特别注意!)
# }
#
# # 不同语言可能需要微调字号 (可选)
# FONT_SIZE_CONFIG = {
#     "zh_cn": 42,
#     "zh_tw": 42,
#     "en": 40,
#     "fr": 40,
#     "de": 40,
#     "ru": 40
# }
#
#
# # =================
#
# def main():
#     # 1. 初始化渲染器 (只加载一次背景图)
#     renderer = DynamicRenderer()
#
#     # 2. 遍历输入源列表
#     for poem_input in POEM_DATA_SOURCE:
#         title_str = poem_input['title']
#         author_str = poem_input['author']
#         print(f"\n=== 开始处理: {title_str} - {author_str} ===")
#
#         # 创建输出目录
#         safe_title = title_str.replace(" ", "_")
#         output_dir = f"./output/{safe_title}_多语言组图"
#         os.makedirs(output_dir, exist_ok=True)
#
#         try:
#             # Step A: 调用 LLM 获取所有数据
#             full_data = fetch_poem_data_v2(title_str, author_str)
#
#             # 保存原始数据备份
#             with open(f"{output_dir}/source_data.json", 'w', encoding='utf-8') as f:
#                 json.dump(full_data, f, ensure_ascii=False, indent=2)
#
#             # 保存小红书文案
#             xhs_copy = full_data.pop("xhs_copy", "No copy generated.")  # 取出并从字典删除
#             with open(f"{output_dir}/小红书文案.txt", 'w', encoding='utf-8') as f:
#                 f.write(xhs_copy)
#             print("✅ 数据获取与文案保存完毕。开始生成图片...")
#
#             # Step B: 循环遍历数据中的 6 种语言，分别生成图片
#             # Step B: 渲染循环
#             data_items = {k: v for k, v in full_data.items() if k != "xhs_copy"}
#
#             for lang_code, lang_data in data_items.items():
#                 if lang_code not in FONT_CONFIG:
#                     continue
#
#                 # === 核心修改点 ===
#                 # 以前是直接用外层的 author_str (中文名)
#                 # 现在从 lang_data 里取 author (AI翻译过的名)
#
#                 poem_title = lang_data.get('title', 'Unknown Title')
#                 poem_content = lang_data.get('content', '')
#
#                 # 优先使用 API 返回的本地化作者名
#                 # 如果 API 偶尔抽风没返回 author 字段，就回退使用输入的中文作者名
#                 poem_author = lang_data.get('author', author_str)
#
#                 font_path = FONT_CONFIG[lang_code]
#
#                 # 构造数据
#                 render_data = {
#                     "title": poem_title,
#                     "author": poem_author,  # <--- 这里变了，现在是多语言作者名
#                     "content": poem_content
#                 }
#
#                 # ... 后面的渲染代码不变 ...
#                 output_img_path = f"{output_dir}/{lang_code}.jpg"
#                 renderer.render(
#                     data=render_data,
#                     font_path=font_path,
#                     output_path=output_img_path,
#                     font_size=40
#                 )
#         except Exception as e:
#             print(f"Error processing {title_str}: {e}")
#             import traceback
#             traceback.print_exc()
#
#
# if __name__ == "__main__":
#     main()

