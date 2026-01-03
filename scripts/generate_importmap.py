from pathlib import Path
import re
import json

import requests
from semantic_version import NpmSpec

packages = (
    "@codemirror/view",
    "@codemirror/state",
    "@codemirror/commands",
    "@codemirror/language",
    "@codemirror/search",
    "@replit/codemirror-vim",
    "@lezer/lr",
)

# TODO: Download source maps and type definitions

if __name__ == "__main__":
    static = Path(__file__).parents[1] / "static"
    importmap = {}
    unvisited = set(packages)
    visited = set()
    while package := unvisited and unvisited.pop():
        visited.add(package)
        metadata = requests.get(f"https://registry.npmjs.org/{package}").json()
        version = metadata["dist-tags"]["latest"]
        package_json = metadata["versions"][version]
        for dep in package_json.get("dependencies", {}).keys():
            if dep not in visited:
                unvisited.add(dep)
        module = requests.get(f"https://cdn.jsdelivr.net/npm/{package}@{version}/+esm").text
        group, _, name = package.rpartition("/")
        path = static / "dist" / group
        path.mkdir(parents=True, exist_ok=True)
        path /= f"{name}.js"
        path.write_text(re.sub(r"/npm/((?:@[a-z0-9-]+/)?[a-z0-9-]+)@\d+.\d+.\d+/\+esm", r"\1", module))
        importmap[package] = f"/{path.relative_to(static).as_posix()}"
    print(json.dumps({"imports": importmap}, indent=4))