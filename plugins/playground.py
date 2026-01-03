from typing import Sequence

from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.utils import OptionsDict, EnvType
from markdown_it.common.utils import escapeHtml, unescapeAll

def playground_plugin(
    md: MarkdownIt,
) -> None:
    md.add_render_rule("fence", playground)

def playground(
    self,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    token = tokens[idx]
    info = unescapeAll(token.info).strip() if token.info else ""
    lang_name = ""
    lang_attrs = ""

    if info:
        arr = info.split(maxsplit=1)
        lang_name = arr[0]
        if len(arr) == 2:
            lang_attrs = arr[1]
    
    if options.highlight:
        highlighted = options.highlight(
            token.content, lang_name, lang_attrs
        ) or escapeHtml(token.content)
    else:
        highlighted = escapeHtml(token.content)

    if highlighted.startswith("<pre"):
        return highlighted + "\n"

    # If language exists, inject class gently, without modifying original token.
    # May be, one day we will add .deepClone() for token and simplify this part, but
    # now we prefer to keep things local.
    if info:
        # Fake token just to render attributes
        tmpToken = Token(type="", tag="", nesting=0, attrs=token.attrs.copy())
        tmpToken.attrJoin("class", options.langPrefix + lang_name)

        return f'<code-mirror lang="{escapeHtml(lang_name)}">{escapeHtml(token.content)}</code-mirror>'

        # return (
        #     "<pre><code"
        #     + self.renderAttrs(tmpToken)
        #     + ">"
        #     + "<span>Injected!</span>"
        #     + highlighted
        #     + "</code></pre>\n"

        #     f"""
        #     <div id="codemirror"></div>
        #     <script type="module">
        #         import {{ EditorView, keymap, lineNumbers, drawSelection, highlightSpecialChars }} from "@codemirror/view"
        #         import {{ defaultKeymap, history, historyKeymap }} from "@codemirror/commands"
        #         import {{ LRLanguage, LanguageSupport, syntaxHighlighting, defaultHighlightStyle }} from "@codemirror/language"
        #         import {{ parser }} from "lezer-lua"
        #         import {{ vim }} from "@replit/codemirror-vim"

        #         const parent = document.getElementById("codemirror");
        #         parent.removeAttribute("id");

        #         const luaLanguage = LRLanguage.define({{
        #           name: "Lua",
        #           parser: parser,
        #           languageData: {{
        #             commentTokens: {{line: "--"}}
        #           }}
        #         }});
        #         console.log(luaLanguage);

        #         const view = new EditorView({{
        #           doc: "{token.content.strip().replace('"', '\\"').replace("\n", "\\n")}",
        #           extensions: [
        #             vim({{}}),
        #             keymap.of([defaultKeymap, historyKeymap]),
        #             lineNumbers(),
        #             history(),
        #             drawSelection(),
        #             highlightSpecialChars(),
        #             syntaxHighlighting(defaultHighlightStyle),
        #             new LanguageSupport(luaLanguage),
        #           ],
        #           parent: parent,
        #         }});

        #         parent.addEventListener("keydown", event => {{
        #             if (event.ctrlKey && event.code === "KeyR") {{
        #                 event.preventDefault();
        #                 const iframe = document.createElement("iframe");
        #                 iframe.src = "player.html";
        #                 iframe.width = 480;
        #                 iframe.height = 270;
        #                 parent.appendChild(iframe);
        #             }}
        #         }});
        #     </script>
        #     <noscript>
        #     <pre><code{self.renderAttrs(token)}>
        #     {highlighted}
        #     </code></pre>
        #     </noscript>
        #     """
        # )

    return (
        "<pre><code"
        + self.renderAttrs(token)
        + ">"
        + highlighted
        + "</code></pre>\n"
    )