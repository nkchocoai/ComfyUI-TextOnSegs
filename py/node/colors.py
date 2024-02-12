from PIL import Image, ImageColor, ImageDraw

import numpy as np
import torch

from .base import BaseNode


class GetComplementaryColor(BaseNode):
    RETURN_TYPES = ("INT", "INT", "INT", "STRING")
    RETURN_NAMES = (
        "r",
        "g",
        "b",
        "hex_color_code",
    )
    FUNCTION = "get_complementary_color"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "r": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "g": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "b": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "threshold": ("INT", {"default": 30, "min": 0, "max": 765, "step": 1}),
                "alt_color_code": ("STRING", {"default": "#000000"}),
            }
        }

    def get_complementary_color(self, r, g, b, threshold, alt_color_code):
        x = min([r, g, b]) + max([r, g, b])
        r2 = x - r
        g2 = x - g
        b2 = x - b
        color_code = f"#{r2:02x}{g2:02x}{b2:02x}"

        if abs(r2 - r) + abs(g2 - g) + abs(b2 - b) < threshold:
            color_code = alt_color_code
            r2, g2, b2 = ImageColor.getcolor(alt_color_code, "RGB")

        return (r2, g2, b2, color_code)


class FloodFill(BaseNode):
    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT")
    RETURN_NAMES = (
        "image",
        "filled_color_r",
        "filled_color_g",
        "filled_color_b",
    )
    FUNCTION = "flood_fill"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "x": ("INT", {"default": 0, "min": 0, "max": 99999, "step": 1}),
                "y": ("INT", {"default": 0, "min": 0, "max": 99999, "step": 1}),
                "pick_color": ("BOOLEAN", {"default": True}),
                "r": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "g": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "b": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "threshold": ("INT", {"default": 50, "min": 0, "max": 1000, "step": 1}),
            }
        }

    def flood_fill(self, image, x, y, pick_color, r, g, b, threshold):
        p = (x, y)

        i = 255.0 * image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        img = img.convert("RGB")
        if pick_color:
            r, g, b = img.getpixel(p)
        self._flood_fill(img, p, (r, g, b), thresh=threshold)

        filled_image = np.array(img).astype(np.float32) / 255.0
        filled_image = torch.from_numpy(filled_image)[None,]
        return filled_image, r, g, b

    # refer. https://github.com/python-pillow/Pillow/blob/5d6f22da122c6620331fd11bc8fd8a88cbc11132/src/PIL/ImageDraw.py#L897
    def _flood_fill(self, image, xy, value, thresh):
        pixel = image.load()

        x, y = xy
        try:
            background = pixel[x, y]
            # if _color_diff(value, background) <= thresh:
            #     return  # seed point already has fill color
            pixel[x, y] = value
        except (ValueError, IndexError):
            return  # seed point outside image
        edge = {(x, y)}
        # use a set to keep record of current and previous edge pixels
        # to reduce memory consumption
        full_edge = set()
        while edge:
            new_edge = set()
            for x, y in edge:  # 4 adjacent method
                for s, t in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    # If already processed, or if a coordinate is negative, skip
                    if (s, t) in full_edge or s < 0 or t < 0:
                        continue
                    try:
                        p = pixel[s, t]
                    except (ValueError, IndexError):
                        pass
                    else:
                        full_edge.add((s, t))
                        fill = self._color_diff(p, background) <= thresh
                        if fill:
                            pixel[s, t] = value
                            new_edge.add((s, t))
            full_edge = edge  # discard pixels processed
            edge = new_edge

    # refer. https://github.com/python-pillow/Pillow/blob/5d6f22da122c6620331fd11bc8fd8a88cbc11132/src/PIL/ImageDraw.py#L1076
    def _color_diff(self, color1, color2) -> float:
        """
        Uses 1-norm distance to calculate difference between two values.
        """
        if isinstance(color2, tuple):
            return sum(abs(color1[i] - color2[i]) for i in range(0, len(color2)))
        else:
            return abs(color1 - color2)
