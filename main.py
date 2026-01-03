from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

from plugins.anchors import anchors_plugin, TocRenderer
from plugins.playground import playground_plugin
from plugins.alerts import alerts_plugin
from plugins.videos import videos_plugin
from plugins.colors import colors_plugin

def copy(src: Path, dest: Path):
    for file in src.iterdir():
        if file.is_dir():
            dir = (dest / file.name)
            dir.mkdir(exist_ok=True)
            copy(file, dir)
        elif file.is_file():
            (dest / file.name).write_bytes(file.read_bytes())
        else:
            raise Exception(f"Unknown dirent type: {file}")

if __name__ == "__main__":
    md = (
        MarkdownIt("gfm-like")
            .use(anchors_plugin, anchor=True)
            .use(footnote_plugin)
            .use(playground_plugin)
            .use(alerts_plugin)
            .use(videos_plugin)
            .use(colors_plugin)
    )

    wiki = Path("wiki")
    files = sorted(filter(lambda p: p.suffix == ".md" and p.name[0] != "_", Path(wiki).iterdir()))
    pages = f"<nav><ul>{"\n".join(f'<li><a href="{file.relative_to(wiki).as_posix()}">{" ".join(map(str.capitalize, file.stem.split()))}</a></li>' for file in files)}</ul></nav>"
    with open("wiki/_Sidebar.md", "r") as page:
        sidebar = md.render(page.read())
    with open("wiki/_Footer.md", "r") as page:
        footer = md.render(page.read())
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("page.html.jinja")

    out = Path("out")
    out.mkdir(exist_ok=True)
    for page in files:
        with open(page, "r") as file:
            tokens = md.parse(file.read())
        content = md.renderer.render(tokens, md.options, {})
        toc = TocRenderer().render(tokens, {}, {})
        html = template.render(content=content, toc=toc, sidebar=sidebar, footer=footer, pages=pages)
        name = "index.html" if page.name == "Home.md" else page.with_suffix(".html")
        (out / "index.html").write_text(html)
    copy(Path("static"), out)
    