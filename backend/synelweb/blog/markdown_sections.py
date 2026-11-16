"""Splits a post's Markdown body into the sections the site shows as cards."""

import re

# A level-two heading ("## Title") starts a new section.
_HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")


def split_sections(body):
    """Return [{"subtitle", "content"}] in order.

    Text before the first heading becomes a section without a subtitle (the
    post's introduction). Headings inside a code block are left alone.
    """
    sections = []
    subtitle = ""
    lines = []
    in_code = False

    def close():
        content = "\n".join(lines).strip()
        if subtitle or content:
            sections.append({"subtitle": subtitle, "content": content})

    for line in (body or "").replace("\r\n", "\n").split("\n"):
        if _FENCE.match(line):
            in_code = not in_code
        heading = None if in_code else _HEADING.match(line)
        if heading:
            close()
            subtitle = heading.group(1)
            lines = []
        else:
            lines.append(line)
    close()
    return sections


def join_sections(sections):
    """The inverse: [(subtitle, content)] as one Markdown body."""
    parts = []
    for subtitle, content in sections:
        subtitle = (subtitle or "").strip()
        content = (content or "").strip()
        block = f"## {subtitle}\n\n{content}" if subtitle else content
        if block.strip():
            parts.append(block.strip())
    return "\n\n".join(parts)
