import os

from PIL import ImageFont

import folder_paths

from .base import BaseNode


def get_font_file_list():
    custom_nodes_dir = os.path.realpath(
        folder_paths.get_folder_paths("custom_nodes")[0]
    )
    font_dir = os.path.join(
        os.path.join(custom_nodes_dir, "ComfyUI_Comfyroll_CustomNodes"), "fonts"
    )
    return [
        f
        for f in os.listdir(font_dir)
        if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")
    ]


class CalcMaxFontSize(BaseNode):
    RETURN_TYPES = (
        "INT",
        get_font_file_list(),
        "INT",
        "INT",
        "INT",
    )
    RETURN_NAMES = (
        "font_size",
        "font_name",
        "text_width",
        "text_height",
        "offset_y",
    )
    FUNCTION = "calc_max_font_size"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": (
                    "INT",
                    {"default": 1024, "min": 0, "max": 99999999, "step": 1},
                ),
                "height": (
                    "INT",
                    {"default": 1024, "min": 0, "max": 99999999, "step": 1},
                ),
                "scale": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 4, "step": 0.05},
                ),
                "text": (
                    "STRING",
                    {"multiline": True},
                ),
                "line_spacing": (
                    "INT",
                    {"default": 0, "min": 0, "max": 99999999, "step": 1},
                ),
                "font_name": (get_font_file_list(),),
            },
        }

    def calc_max_font_size(self, width, height, scale, text, line_spacing, font_name):
        font_size = 1
        text_width = 0
        text_height = 0
        previous_text_width = 0
        previous_text_height = 0
        text_height = 0

        lines = text.splitlines()
        line_spacing_height = line_spacing * (len(lines) - 1)

        while True:
            font_folder = "fonts"
            font_file = os.path.join(font_folder, font_name)
            custom_nodes_dir = os.path.realpath(
                folder_paths.get_folder_paths("custom_nodes")[0]
            )
            resolved_font_path = os.path.join(
                os.path.join(custom_nodes_dir, "ComfyUI_Comfyroll_CustomNodes"),
                font_file,
            )
            font = ImageFont.truetype(str(resolved_font_path), font_size)

            w = 0
            h = line_spacing_height
            for line in lines:
                x1, y1, x2, y2 = font.getbbox(line)
                w = max(w, x2 - x1)
                h += y2 - y1
            text_width = w
            text_height = h
            if text_width > width * scale or text_height > height * scale:
                font_size -= 1
                text_width = previous_text_width
                text_height = previous_text_height
                break
            font_size += 1
            previous_text_width = text_width
            previous_text_height = text_height

        offset_y = text_height / 2 / (len(lines) + 1)
        offset_y -= line_spacing_height / 2
        print(font_size, font_name, text_width, text_height, offset_y)

        return (font_size, font_name, text_width, text_height, offset_y)
