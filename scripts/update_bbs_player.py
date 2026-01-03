#!/usr/bin/env python3

import sys
from pathlib import Path

import requests

if __name__ == "__main__":

    # TODO: Figure out latest version automatically
    version = sys.argv[1] if len(sys.argv) > 1 else "0100g"

    dir = Path(__file__).parents[1] / "static" / "play"
    dir.mkdir(exist_ok=True)
    (dir / "picotron.wasm").write_bytes(requests.get(f"https://www.lexaloffle.com/play/picotron_{version}.wasm").content)
    # TODO: Patch to rename `picotron.wasm` or do something smarter
    (dir / "picotron.js").write_bytes(requests.get(f"https://www.lexaloffle.com/play/picotron_{version}.js").content)