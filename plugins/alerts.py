from enum import Enum, auto
from typing import Optional, Sequence

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token
from markdown_it.utils import OptionsDict, EnvType

def alerts_plugin(
    md: MarkdownIt,
) -> None:
    
    class Alert(Enum):
        NOTE = auto()
        TIP = auto()
        IMPORTANT = auto()
        WARNING = auto()
        CAUTION = auto()

        def __str__(self) -> str:
            return self.name.lower()
    
    def rule(state: StateCore) -> None:
        tokens = state.tokens
        for i in range(0, len(tokens) - 3):
            if alert := try_alert(tokens, i):
                tokens[i].type = "alert"
                tokens[i].info = alert
                tokens[i].nesting = 1
                tokens[i + 2].content = tokens[i + 2].content.partition("\n")[2]

    def try_alert(tokens: list[Token], index: int) -> Optional[Alert]:
        if tokens[index].type == "blockquote_open" and \
            tokens[index + 1].type == "paragraph_open" and \
            tokens[index + 2].type == "inline":
            match tokens[index + 2].content.partition("\n")[0].strip().lower():
                case "[!note]":
                    return Alert.NOTE
                case "[!tip]":
                    return Alert.TIP
                case "[!important]":
                    return Alert.IMPORTANT
                case "[!warning]":
                    return Alert.WARNING
                case "[!caution]":
                    return Alert.CAUTION
    
    def render(
        self,
        tokens: Sequence[Token],
        index: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        token = tokens[index]
        assert token.block and token.nesting == 1
        return f'<blockquote class="alert alert-{token.info}">\n'

    md.core.ruler.after("block", "alert", rule)
    md.add_render_rule("alert", render)
