import math
import random
from PIL import Image, ImageDraw, ImageFilter


def create_dynamic_background(width=1242, target_height=1660):
    """
    根据指定的高度，动态生成一张带玫瑰暗纹和噪点的信纸背景。
    :param width: 固定宽度 1242
    :param target_height: 动态高度，至少 1660，长诗会自动增加
    :return: PIL.Image 对象
    """
    # 确保高度不小于标准高度
    height = max(1660, int(target_height))

    # print(f"🎨 正在生成动态背景 (尺寸: {width}x{height})...")

    # === 1. 生成渐变底色 ===
    c_center = (255, 253, 250)  # 中心暖白
    c_edge = (245, 235, 225)  # 边缘米色

    img = Image.new("RGB", (width, height), c_center)
    pixels = img.load()

    # 调整渐变中心点：如果是长图，中心点稍微靠上一点，视觉重心更稳
    center_x = width / 2
    center_y = min(height / 2, 830)  # 视觉中心保持在上方区域，不要跑到底部去

    # 计算渐变半径 (如果是长图，为了防止底部全黑，适当拉长最大距离)
    max_dist = math.sqrt(center_x ** 2 + (height * 0.8) ** 2)

    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            dist = math.sqrt(dx * dx + dy * dy)
            ratio = min(dist / max_dist, 1.0)

            # 颜色插值
            r = int(c_center[0] * (1 - ratio) + c_edge[0] * ratio)
            g = int(c_center[1] * (1 - ratio) + c_edge[1] * ratio)
            b = int(c_center[2] * (1 - ratio) + c_edge[2] * ratio)
            pixels[x, y] = (r, g, b)

    # === 2. 绘制玫瑰暗纹 (平铺) ===
    # 这一步非常适合长图，只要循环次数变多即可
    pattern_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pattern_draw = ImageDraw.Draw(pattern_layer)

    step_x, step_y = 300, 300
    pattern_color = (180, 160, 150, 15)  # 极淡的暗纹

    for y in range(0, height + step_y, step_y):
        for x in range(0, width + step_x, step_x):
            offset_x = x + random.randint(-30, 30)
            offset_y = y + random.randint(-30, 30)
            if (y // step_y) % 2 == 1: offset_x += step_x // 2

            # 简单的花瓣模拟
            size = random.randint(80, 120)
            for i in range(5):
                angle = math.radians(72 * i)
                px = offset_x + math.cos(angle) * (size * 0.3)
                py = offset_y + math.sin(angle) * (size * 0.3)
                pattern_draw.ellipse((px - size * 0.4, py - size * 0.4, px + size * 0.4, py + size * 0.4),
                                     fill=pattern_color)

    img.paste(pattern_layer, (0, 0), mask=pattern_layer)

    # === 3. 添加纸张颗粒感 ===
    # 为了性能，长图可以只生成局部噪音然后平铺，或者直接生成大噪音图
    # 这里为了质量，我们还是生成全尺寸噪音，可能会稍微慢1秒
    noise_img = Image.effect_noise((width, height), 15).convert("RGB")
    img = Image.blend(img, noise_img, 0.03)

    return img