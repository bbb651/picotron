import re
from typing import Any, Callable, Optional, Sequence, cast

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token
from markdown_it.renderer import RendererProtocol
from markdown_it.utils import OptionsDict, EnvType


def anchors_plugin(
    md: MarkdownIt,
    min_level: int = 1,
    max_level: int = 2,
    slug_func: Optional[Callable[[str], str]] = None,
    anchor: bool = False,
) -> None:
    """Plugin for adding header anchors, based on
    `markdown-it-anchor <https://github.com/valeriangalliat/markdown-it-anchor>`__

    .. code-block:: md

        # Title String

    renders as:

    .. code-block:: html

        <h1 id="title-string"><a href="#title-string">Title String</a></h1>

    :param min_level: minimum header level to apply anchors
    :param max_level: maximum header level to apply anchors
    :param slug_func: function to convert title text to id slug.
    :param anchor: wrap the header child in a permalink

    Note, the default slug function aims to mimic the GitHub Markdown format, see:

    - https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb
    - https://gist.github.com/asabaylus/3071099

    """
    selected_levels = list(range(min_level, max_level + 1))
    md.core.ruler.push(
        "anchor",
        _make_anchors_func(
            selected_levels,
            slug_func or slugify,
            anchor,
        ),
    )


def _make_anchors_func(
    selected_levels: list[int],
    slug_func: Callable[[str], str],
    anchor,
) -> Callable[[StateCore], None]:
    def _anchor_func(state: StateCore) -> None:
        slugs: set[str] = set()
        for index, token in enumerate(state.tokens):
            if token.type != "heading_open":
                continue
            level = int(token.tag[1])
            if level not in selected_levels:
                continue
            inline_token = state.tokens[index + 1]
            assert inline_token.children is not None
            title = "".join(
                child.content
                for child in inline_token.children
                if child.type in ["text", "code_inline"]
            )
            slug = unique_slug(slug_func(title), slugs)
            token.attrSet("id", slug)

            if anchor:
                state.tokens.insert(index + 1, Token(
                    type="link_open",
                    tag="a",
                    nesting=1,
                    attrs={"href": f"#{slug}"},
                    children=inline_token.children,
                ))
                state.tokens.insert(index + 3, Token(
                    type="link_close",
                    tag="a",
                    nesting=-1,
                ))
    return _anchor_func


def slugify(title: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff\- ]", "", title.strip().lower().replace(" ", "-"))


def unique_slug(slug: str, slugs: set[str]) -> str:
    uniq = slug
    i = 1
    while uniq in slugs:
        uniq = f"{slug}-{i}"
        i += 1
    slugs.add(uniq)
    return uniq


class TocRenderer(RendererProtocol):
    def render(
        _self, tokens: Sequence[Token], _options: OptionsDict, _env: EnvType
    ) -> Any:
        result = "<ol>\n"
        for i, token in enumerate(tokens):
            if token.type == "heading_open" and (id := token.attrGet("id")):
                result += f'<nav><li><a href="#{id}">{"".join(child.content for child in tokens[i + 1].children)}</a></li></nav>\n'
        result += "</ol>"
        return result