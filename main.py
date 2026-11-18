#!/usr/bin/env python3
"""Copy the pre-drawn entry image to the output directory (stdlib only)."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(HERE, "out"))
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    print("wrote", os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
