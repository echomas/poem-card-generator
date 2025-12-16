from PIL import Image


def prepare_background(input_path, output_path):
    # 1. 打开原始 AI 生成的图
    img = Image.open(input_path)

    # 2. 目标尺寸 (小红书 3:4)
    target_width = 1242
    target_height = 1660

    # --- 策略 A: 裁剪中间部分 (推荐，保留纹理) ---
    # 先把高度缩放到目标高度，宽度等比缩放
    ratio = target_height / img.height
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)

    if new_w < target_width:
        # 如果缩放后宽度不够，就按宽度缩放
        ratio = target_width / img.width
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)

    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    # 计算裁剪框 (居中裁剪)
    left = (img_resized.width - target_width) / 2
    top = (img_resized.height - target_height) / 2
    right = (img_resized.width + target_width) / 2
    bottom = (img_resized.height + target_height) / 2

    img_final = img_resized.crop((left, top, right, bottom))

    # --- 策略 B: 如果你想旋转90度 (适合无方向的纹理) ---
    # img_final = img.rotate(90, expand=True).resize((target_width, target_height))

    # 3. 保存
    img_final.save(output_path, quality=95)
    print(f"背景图已处理: {output_path} ({target_width}x{target_height})")


# 运行一次
# prepare_background("./assets/templates/paper_bg.png", "./assets/templates/paper_bg.png")