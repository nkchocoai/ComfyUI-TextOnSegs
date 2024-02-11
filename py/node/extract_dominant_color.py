from PIL import Image

import numpy as np

from .base import BaseNode


class ExtractDominantColor(BaseNode):
    RETURN_TYPES = ("INT", "INT", "INT", "STRING")
    RETURN_NAMES = (
        "r",
        "g",
        "b",
        "hex_color_code",
    )
    FUNCTION = "extract_dominant_color"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    def extract_dominant_color(self, image):
        i = 255.0 * image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # refer. https://stackoverflow.com/a/59507814
        reduced = img.convert("P", palette=Image.WEB)
        palette = reduced.getpalette()
        palette = [palette[3 * n : 3 * n + 3] for n in range(256)]
        color_count = [(n, palette[m]) for n, m in reduced.getcolors()]
        color_count.sort(key=lambda x: x[0], reverse=True)

        print(color_count)
        r, g, b = color_count[0][1]
        hex_color_code = f"#{r:02x}{g:02x}{b:02x}"

        return (r, g, b, hex_color_code)
