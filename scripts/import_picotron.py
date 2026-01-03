
import sys
from pathlib import Path
from typing import Any, Iterator

import requests
from requests import RequestException

def iter_repo(url = "https://api.github.com/repos/Picotron-Software-Developers/Picotron-Wiki/contents/?ref=main") -> Iterator[tuple[Path, str]]:
    response = requests.get(url).json()
    assert type(response) is list
    for file in response:
        if file["type"] == "dir":
            yield from iter_repo(file["url"])
        elif file["type"] == "file":
            try:
                path = Path(file["path"]).with_suffix(".md")
                download_url: str = file["download_url"]
                markdown = parse_page(path.name, requests.get(download_url).json())
                yield path, markdown
            except RequestException:
                print(f"warning: failed to download, skipping: {file}", file=sys.stderr)
        else:
            print(f"warning: file has unknown type, skipping: {file}", file=sys.stderr)

def parse_page(filename: str, contents: dict[str, Any]) -> str:
    metadata: dict[str, Any] = contents["metadata"]
    page_title = metadata.get("page_title") or " ".join(map(str.capitalize, filename.split("_")))
    authors = metadata.get("authors")
    if authors:
        authors = f"## Authors: {", ".join(authors)}\n\n"
    version = metadata.get("version")
    if version:
        version = f"## Version: {version}\n\n"

    elements = contents["elements"]
    paragraphs = []
    for element in elements:
        match element["type"]:
            case "label":
                paragraphs.append(element["text"])
            case "snippet" | "demo":
                paragraphs.append(f"```lua\n{element["text"]}\n```")
            case "dir_ref":
                paragraphs.append(f"{element["text"]}: `{element["ref"]}`")
            case "wiki_ref":
                paragraphs.append(f"[{element["text"]}]({element["ref"]})")
            case "pod_image":
                paragraphs.append(f"![{element["text"]}](data:pod;base64,{element["data"].removeprefix("b64:")})")
            case "note":
                paragraphs.append(f"> [!NOTE]\n > {element["text"]}")
            case _:
                raise ValueError("Unknown element type")
    return f"# {page_title}\n\n{authors or ""}{version or ""}{"\n\n".join(paragraphs)}"

if __name__ == "__main__":
    dir = Path(__file__).parent / "wiki"
    dir.mkdir(exist_ok=True)
    for file, markdown in iter_repo():
        page_path = (dir / file)
        page_path.parent.mkdir(parents=True, exist_ok=True)
        page_path.write_text(markdown)