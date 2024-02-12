from .py.node.calc_max_font_size import CalcMaxFontSize
from .py.node.segs_to_region import SegsToRegion
from .py.node.extract_dominant_color import ExtractDominantColor
from .py.node.colors import GetComplementaryColor, FloodFill

NODE_CLASS_MAPPINGS = {
    "SegsToRegion": SegsToRegion,
    "CalcMaxFontSize": CalcMaxFontSize,
    "ExtractDominantColor": ExtractDominantColor,
    "GetComplementaryColor": GetComplementaryColor,
    "TextOnSegsFloodFill": FloodFill,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SegsToRegion": "SegsToRegion",
    "CalcMaxFontSize": "CalcMaxFontSize",
    "ExtractDominantColor": "ExtractDominantColor",
    "GetComplementaryColor": "GetComplementaryColor",
    "TextOnSegsFloodFill": "FloodFill",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
