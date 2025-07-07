from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import textwrap
import numpy as np

def add_text_to_video(video_path, output_path, text,
                      font_path=os.path.join("fonts", "RedHatDisplay-Italic-VariableFont_wght.ttf"),
                      max_font_size=120, min_font_size=20,
                      max_width_ratio=0.8,
                      max_height_ratio=0.3,
                      duration=None):
    video = VideoFileClip(video_path)

    max_width = int(video.w * max_width_ratio)
    max_height = int(video.h * max_height_ratio)

    def fit_text_to_box(text, font_path, max_width, max_height, max_font_size, min_font_size):
        font_size = max_font_size
        wrapped_lines = None
        font = None

        while font_size >= min_font_size:
            font = ImageFont.truetype(font_path, font_size)
            wrapper = textwrap.TextWrapper(width=40)
            wrapped_lines = wrapper.wrap(text)

            max_line_width = 0
            total_height = 0
            for line in wrapped_lines:
                w, h = font.getbbox(line)[2:4]
                max_line_width = max(max_line_width, w)
                total_height += h + 5

            if max_line_width <= max_width and total_height <= max_height:
                break

            font_size -= 2

        return font, wrapped_lines, max_line_width, total_height

    font, wrapped_lines, _, text_h = fit_text_to_box(text, font_path, max_width, max_height, max_font_size, min_font_size)

    img_width = video.w
    img_height = text_h + 20
    img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y_text = 10
    for line in wrapped_lines:
        line_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        x = (img_width - line_width) // 2
        y = y_text

        # Dış çizgi
        outline_range = 2
        for dx in range(-outline_range, outline_range + 1):
            for dy in range(-outline_range, outline_range + 1):
                if dx == 0 and dy == 0:
                    continue
                draw.text((x + dx, y + dy), line, font=font, fill="black")

        draw.text((x, y), line, font=font, fill="white")
        y_text += font.getbbox(line)[3] - font.getbbox(line)[1] + 5

    img_array = np.array(img)

    text_clip = ImageClip(img_array).with_duration(duration or video.duration)
    text_clip = text_clip.with_position(("center", "center"))

    final = CompositeVideoClip([video, text_clip])
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')
