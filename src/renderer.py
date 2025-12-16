import re
from PIL import Image, ImageDraw, ImageFont
from src.dynamic_bg import create_dynamic_background  # 引入刚才写的背景模块


# 如果尚未安装 langdetect，请先 pip install langdetect
# from langdetect import detect

class DynamicRenderer:
    def __init__(self):
        # 基础配置
        self.width = 1242  # 固定宽度
        self.margin_x = 140
        self.content_width = self.width - (self.margin_x * 2)

        # 颜色配置
        self.ink_color = (60, 50, 50, 230)
        self.title_color = (40, 40, 50, 240)

        # 布局配置
        self.y_title = 200  # 标题起始Y
        self.y_author = 320  # 作者起始Y
        self.y_body_start = 480  # 正文起始Y
        self.padding_bottom = 250  # 底部留白

    def _get_font(self, font_path, size):
        try:
            return ImageFont.truetype(font_path, int(size))
        except:
            return ImageFont.load_default()

    def _layout_text(self, text, font, line_spacing_ratio=0.6, para_spacing_ratio=1.2):
        """
        计算文本排版布局
        返回: (layout_structure, total_pixel_height)
        """
        paragraphs = text.split('\n')
        layout_data = []

        ascent, descent = font.getmetrics()
        font_height = ascent + descent
        line_gap = font_height * line_spacing_ratio
        para_gap = font_height * para_spacing_ratio

        total_height = 0

        for para in paragraphs:
            para = para.strip()
            if not para: continue

            # 简单的中西文分词判断
            is_latin = any('a' <= char.lower() <= 'z' for char in para)
            words = para.split(' ') if is_latin else list(para)

            current_line = ""
            para_lines = []

            for word in words:
                sep = " " if is_latin else ""
                test_line = current_line + sep + word if current_line else word
                if font.getlength(test_line) <= self.content_width:
                    current_line = test_line
                else:
                    para_lines.append(current_line)
                    current_line = word
            if current_line: para_lines.append(current_line)

            # 计算本段落高度
            p_height = len(para_lines) * font_height + (len(para_lines) - 1) * line_gap

            layout_data.append({
                "lines": para_lines,
                "height": p_height,
                "font_height": font_height,
                "line_gap": line_gap
            })
            total_height += p_height

        # 加上段落间距
        if len(layout_data) > 1:
            total_height += (len(layout_data) - 1) * para_gap

        return layout_data, total_height, para_gap

    def render(self, data, font_path, output_path, font_size=40):
        # 1. 准备字体
        font_title = self._get_font(font_path, 75)
        font_author = self._get_font(font_path, 38)
        font_body = self._get_font(font_path, font_size)  # 锁定字号，不再缩小！

        # 2. 虚拟排版 (只计算高度，不画图)
        print(f"  ...正在计算诗歌 [{data['title'][:5]}] 的长度需求...")
        layout, body_height, para_gap = self._layout_text(data['content'], font_body)

        # 3. 计算所需的总画布高度
        # 公式: 正文起始位置 + 正文实际高度 + 底部留白
        required_height = self.y_body_start + body_height + self.padding_bottom

        # 4. 生成动态底图
        # 如果需要的高度(比如1800) > 标准(1660)，就用1800；否则用1660
        final_height = max(1660, int(required_height))

        print(f"  ...生成底图: {self.width}x{final_height} px (内容高: {int(body_height)} px)")
        img = create_dynamic_background(self.width, final_height)
        draw = ImageDraw.Draw(img)

        # 5. 正式绘制

        # A. 标题 (居中)
        w_title = font_title.getlength(data['title'])
        draw.text(((self.width - w_title) / 2, self.y_title), data['title'], font=font_title, fill=self.title_color)

        # B. 作者 (居中)
        author_str = f"— {data['author']}"
        w_auth = font_author.getlength(author_str)
        draw.text(((self.width - w_auth) / 2, self.y_author), author_str, font=font_author, fill=(100, 100, 100, 200))

        # C. 正文 (根据 layout 数据绘制)
        # 如果是标准高度图片，我们让短诗在中间区域视觉居中
        # 如果是长图，就从固定的 y_body_start 开始写，保证头部统一
        if final_height == 1660:
            # 短诗：垂直居中微调
            available_space = 1660 - self.y_body_start - self.padding_bottom
            extra_margin = max(0, (available_space - body_height) / 2)
            cursor_y = self.y_body_start + extra_margin
        else:
            # 长诗：固定顶端
            cursor_y = self.y_body_start

        for para in layout:
            f_h = para['font_height']
            l_gap = para['line_gap']
            for line in para['lines']:
                w_line = font_body.getlength(line)
                draw.text(((self.width - w_line) / 2, cursor_y), line, font=font_body, fill=self.ink_color)
                cursor_y += f_h + l_gap
            cursor_y -= l_gap  # 撤销最后一行多加的行距
            cursor_y += para_gap  # 加上段距

        # 6. 保存
        img.save(output_path, quality=95)
        print(f"✅ 图片已保存: {output_path}")