from .base import BaseNode


class SegsToRegion(BaseNode):
    RETURN_TYPES = ("INT", "INT", "INT", "INT", "INT", "INT", "INT", "INT", "BOOLEAN")
    RETURN_NAMES = (
        "x1",
        "y1",
        "x2",
        "y2",
        "width",
        "height",
        "center_x",
        "center_y",
        "is_found",
    )
    FUNCTION = "segs_to_region"

    RETURN_VALUES_IF_NOT_FOUND = (0, 0, 0, 0, False)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "segs": ("SEGS",),
                "index": ("INT", {"default": 0, "min": 0, "max": 99999999, "step": 1}),
            }
        }

    def segs_to_region(self, segs, index):
        if len(segs[1]) <= index:
            return self.RETURN_VALUES_IF_NOT_FOUND

        seg = segs[1][index]
        x1, y1, x2, y2 = [int(v) for v in seg.bbox]
        w = x2 - x1
        h = y2 - y1
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        return (x1, y1, x2, y2, w, h, cx, cy, True)
