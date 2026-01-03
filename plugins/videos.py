from typing import Sequence
import re

from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.utils import OptionsDict, EnvType

def videos_plugin(
    md: MarkdownIt,
) -> None:

    def render_video_open(
        self,
        tokens: Sequence[Token],
        index: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        paragraph = self.renderToken(tokens, index, options, env)
        if index + 2 < len(tokens) and tokens[index + 1].type == "inline" and tokens[index + 2].type == "paragraph_close" and \
            len(tokens[index + 1].children) > 2 and tokens[index + 1].children[0].type == "link_open" and \
            tokens[index + 1].children[1].type == "text" and tokens[index + 1].children[2].type == "link_close":

            href = tokens[index + 1].children[0].attrGet("href")
            # List from https://gist.github.com/aaomidi/0a3b5c9bd563c9e012518b495410dc0e
            if re.search(r"\.(webm|mkv|flv|vob|ogv|ogg|rrc|gifv|mng|mov|avi|qt|wmv|yuv|rm|asf|amv|mp4|m4p|m4v|mpg|mp2|mpeg|mpe|mpv|m4v|svi|3gp|3g2|mxf|roq|nsv|flv|f4v|f4p|f4a|f4b|mod)$", href):
                tokens[index + 2].meta["video"] = True
                return f'<video controls src={href}>{paragraph}'
        return paragraph

    def render_video_close(
        self,
        tokens: Sequence[Token],
        index: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        paragraph = self.renderToken(tokens, index, options, env)
        if tokens[index].meta.get("video"):
            return f'{paragraph}</video>'
        return paragraph

    md.add_render_rule("paragraph_open", render_video_open)
    md.add_render_rule("paragraph_close", render_video_close)