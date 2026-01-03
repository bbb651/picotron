import colorsys
import re
from typing import Optional, Sequence, Iterable, Callable, Final

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token
from markdown_it.utils import OptionsDict, EnvType

type Color = tuple[int, int, int]
type Parser = Callable[[str], Optional[Color]]

def parse_hex(color: str) -> Optional[Color]:
    length = len(color)
    if not length or color[0] != "#":
        return None
    try:
        match length:
            case 4:
                return tuple(int(color[i+1:i+2], 16) * 0x11 for i in range(3))
            case 7:
                return tuple(int(color[i+1:i+3], 16) for i in range(3))
            case _:
                return None
    except ValueError:
        return None

def parse_rgb(color: str) -> Optional[Color]:
    if match := re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", color):
        try:
            r, g, b = filter(lambda c: 0 <= c < 256, map(int, match.groups()))
            return r, g, b
        except ValueError:
            return None

def parse_hsl(color: str) -> Optional[Color]:
    if match := re.match(r"hsl\((\d+),\s*(\d+),\s*(\d+)\)", color):
        try:
            h, s, l = filter(lambda c: 0 <= c < 256, map(int, match.groups()))
            r, g, b = colorsys.hls_to_rgb(h / 255, s / 255, l / 255)
            return int(r * 255), int(g * 255), int(b * 255)
        except ValueError:
            return None

BUILTIN_PARSERS: Final[tuple[Parser]] = (
    parse_hex,
    parse_rgb,
    parse_hsl
)

def colors_plugin(
    md: MarkdownIt,
    parsers: Iterable[Parser] = (),
    builtin_parsers: bool = True,
) -> None:
    parsers = list(*parsers, *BUILTIN_PARSERS) if parsers else BUILTIN_PARSERS
    def parse(content):
        for parser in parsers:
            if color := parser(content):
                r, g, b = color
                return f"#{r:02x}{g:02x}{b:02x}"

    def render(
        self,
        tokens: Sequence[Token],
        index: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        token = tokens[index]
        if color := parse(token.content):
            token.attrPush(("data-color", color))
            token.attrPush(("style", f"--color: {color};"))
        return self.code_inline(tokens, index, options, env)
    md.add_render_rule("code_inline", render)

