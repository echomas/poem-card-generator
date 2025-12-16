import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter


def create_textured_paper(width=1242, height=1660):
    print("🎨 正在调配颜料 (1/3): 生成柔光渐变底色...")

    # === 1. 生成渐变底色 ===
    c_center = (255, 253, 250)  # 中心暖白
    c_edge = (245, 235, 225)  # 边缘米色

    img = Image.new("RGB", (width, height), c_center)
    pixels = img.load()

    center_x, center_y = width / 2, height / 2
    max_dist = math.sqrt(center_x ** 2 + center_y ** 2)

    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            dist = math.sqrt(dx * dx + dy * dy)
            ratio = min(dist / max_dist, 1.0)

            r = int(c_center[0] * (1 - ratio) + c_edge[0] * ratio)
            g = int(c_center[1] * (1 - ratio) + c_edge[1] * ratio)
            b = int(c_center[2] * (1 - ratio) + c_edge[2] * ratio)
            pixels[x, y] = (r, g, b)

    print("🌹 正在压印纹理 (2/3): 绘制玫瑰暗纹...")

    # === 2. 绘制玫瑰花/花卉暗纹 ===
    # 创建一个透明图层专门画花纹
    pattern_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pattern_draw = ImageDraw.Draw(pattern_layer)

    # 设定花纹参数
    step_x = 300  # 花朵横向间距
    step_y = 300  # 花朵纵向间距

    # 玫瑰暗纹的颜色 (比底色稍深一点点的暖灰)
    # 关键在于 Alpha 通道 (最后一位)，设得很低 (15-25)，模拟“隐隐约约”的感觉
    pattern_color = (180, 160, 150, 15)

    for y in range(0, height + step_y, step_y):
        for x in range(0, width + step_x, step_x):
            # 给每个花的位置加一点随机偏移，不要太死板
            offset_x = x + random.randint(-30, 30)
            offset_y = y + random.randint(-30, 30)

            # 交错排列 (像墙纸一样)
            if (y // step_y) % 2 == 1:
                offset_x += step_x // 2

            # === 画一个抽象玫瑰 (由多个重叠的圆弧组成) ===
            size = random.randint(80, 120)  # 花的大小

            # 画5片“花瓣”
            for i in range(5):
                # 计算花瓣圆心
                angle = math.radians(72 * i)
                petal_x = offset_x + math.cos(angle) * (size * 0.3)
                petal_y = offset_y + math.sin(angle) * (size * 0.3)
                petal_r = size * 0.4

                # 绘制实心圆作为花瓣
                pattern_draw.ellipse(
                    (petal_x - petal_r, petal_y - petal_r,
                     petal_x + petal_r, petal_y + petal_r),
                    fill=pattern_color, outline=None
                )

            # 画“花蕊”
            pattern_draw.ellipse(
                (offset_x - size * 0.15, offset_y - size * 0.15,
                 offset_x + size * 0.15, offset_y + size * 0.15),
                fill=pattern_color
            )

    # 将花纹层叠加到底图上
    img.paste(pattern_layer, (0, 0), mask=pattern_layer)

    print("📜 正在做旧处理 (3/3): 添加纸张颗粒感...")

    # === 3. 添加纸张颗粒噪音 (Paper Grain) ===
    # 这步能消除“电脑绘图”的廉价感
    # 我们生成一个噪音层，然后混合
    noise_img = Image.effect_noise((width, height), 15)  # 强度15
    noise_img = noise_img.convert("RGB")

    # 将噪音层变成半透明并叠加
    # 这里我们手动把噪音混合进去，太复杂的混合模式PIL不支持，我们用简单的方法：
    # 直接在原像素上微调
    pixels = img.load()
    noise_pixels = noise_pixels = noise_img.load()

    # 为了速度，我们只随机抽取一些点或者用 Image.blend
    # 更好的方法是用 PIL 的 blend
    blend_layer = Image.blend(img, noise_img, 0.03)  # 3% 的噪音混合

    # 保存
    output_dir = "./assets/templates"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/paper_rose_texture.jpg"
    blend_layer.save(output_path, quality=95)

    print(f"✅ 高级信纸已生成: {output_path}")


if __name__ == "__main__":
    create_textured_paper()