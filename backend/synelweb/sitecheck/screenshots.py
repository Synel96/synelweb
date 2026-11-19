"""What the phone (or desktop) shows while the page loads, from Lighthouse.

The final screenshot and a short filmstrip of the loading, as data URIs
(JPEG/WebP/PNG only, size-capped: they go straight into the visitor's
browser and the cache).
"""

import re

MAX_FRAMES = 8
MAX_IMAGE_CHARS = 250_000
_DATA_URI = re.compile(r"^data:image/(jpeg|webp|png);base64,[A-Za-z0-9+/=]+$")


def _image(value):
    if isinstance(value, str) and len(value) <= MAX_IMAGE_CHARS and _DATA_URI.match(value):
        return value
    return None


def screenshots(lighthouse):
    audits = lighthouse.get("audits") or {}
    frames = []
    for item in ((audits.get("screenshot-thumbnails") or {}).get("details") or {}).get("items") or []:
        data = _image(item.get("data"))
        if data:
            frames.append({"timing": round(item.get("timing") or 0), "data": data})
    if len(frames) > MAX_FRAMES:
        # Keep the first and the last, evenly spread in between.
        step = (len(frames) - 1) / (MAX_FRAMES - 1)
        frames = [frames[round(index * step)] for index in range(MAX_FRAMES)]

    final = _image(((audits.get("final-screenshot") or {}).get("details") or {}).get("data"))
    if not final and frames:
        final = frames[-1]["data"]
    return {"final": final, "filmstrip": frames}
