#!/usr/bin/env python3
"""THE TWO SHORES TIMES - entrypoint.

Copy-only program: writes the embedded front page (entry.png, stored
beside this file in the repository) to /output/entry.png.
Python standard library only, no network. Running it twice writes
byte-identical output because it copies one fixed file.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.exists(src):
        src = os.path.join(os.getcwd(), "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
