import { EditorView, keymap, lineNumbers, drawSelection, highlightSpecialChars } from "@codemirror/view"
import { defaultKeymap, history, historyKeymap } from "@codemirror/commands"
import { LRLanguage, LanguageSupport, syntaxHighlighting, defaultHighlightStyle } from "@codemirror/language"
import { parser } from "lezer-lua"
import { vim } from "@replit/codemirror-vim"

const luaLanguage = LRLanguage.define({
    name: "Lua",
    parser: parser,
    languageData: {
        commentTokens: {line: "--"}
    }
});

class CodeMirror extends HTMLElement {
    static observedAttributes = ["value", "lang"]

    constructor() {
        super()
        this.attachShadow({ mode: "open" });
    }

    connectedCallback() {
        const code = this.textContent;
        const lang = this.getAttribute('lang');

        this.view = new EditorView({
            doc: code,
            extensions: [
                vim(),
                keymap.of([defaultKeymap, historyKeymap]),
                lineNumbers(),
                history(),
                drawSelection(),
                highlightSpecialChars(),
                syntaxHighlighting(defaultHighlightStyle),
                new LanguageSupport(luaLanguage),
            ],
            parent: this.shadowRoot,
            root: this.shadowRoot,
        });
        console.log("Shadow root!");

    }

    // disconnectedCallback() {

    // }

    // adoptedCallback() {

    // }

    // attributeChangedCallback(name, oldValue, newValue) {
    //     console.log(`attributeChangedCallback(${name}, ${oldValue}, ${newValue})`);
    // }
}

customElements.define("code-mirror", CodeMirror);