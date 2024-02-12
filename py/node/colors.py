from PIL import ImageColor

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
