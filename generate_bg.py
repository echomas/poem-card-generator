import os
import math
from PIL import Image, ImageDraw


def create_soft_paper_bg(width=1242, height=1660):
    # 1. 准备参数
    # 核心颜色：中心是极亮的暖白，四周是柔和的米色
    c_center = (255, 253, 250)
    c_edge = (245, 235, 225)

    print("正在生成渐变背景，这可能需要几秒钟...")

    # 2. 创建画布
    img = Image.new("RGB", (width, height), c_center)
    pixels = img.load()

    # 3. 像素级渲染径向渐变
    center_x, center_y = width / 2, height / 2
    # 计算最大距离（从中心到角落），用于归一化
    max_dist = math.sqrt(center_x ** 2 + center_y ** 2)

    for y in range(height):
        for x in range(width):
            # 计算当前点到中心的距离
            dx = x - center_x
            dy = y - center_y
            dist = math.sqrt(dx * dx + dy * dy)

            # 计算渐变比例 (0.0=中心, 1.0=边缘)
            ratio = min(dist / max_dist, 1.0)

            # 增加一点平滑曲线 (可选，让中间亮部范围更大一点)
            # ratio = ratio * ratio

            # 颜色插值算法
            r = int(c_center[0] * (1 - ratio) + c_edge[0] * ratio)
            g = int(c_center[1] * (1 - ratio) + c_edge[1] * ratio)
            b = int(c_center[2] * (1 - ratio) + c_edge[2] * ratio)

            pixels[x, y] = (r, g, b)

    # 4. 保存文件
    output_dir = "./assets/templates"
    os.makedirs(output_dir, exist_ok=True)  # 防止目录不存在报错

    output_path = f"{output_dir}/paper_clean.jpg"
    img.save(output_path, quality=95)
    print(f"✅ 背景图已成功生成: {output_path}")


if __name__ == "__main__":
    create_soft_paper_bg()