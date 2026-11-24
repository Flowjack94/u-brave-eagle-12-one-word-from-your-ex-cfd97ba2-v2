#!/usr/bin/env python3
"""One Word From Your Ex — make.fun entry.

Writes exactly one word to /output/entry.txt: the word an ex would
use to describe the author. Nothing else.
"""

import os
import re

WORD = "placeholder"
OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    # Exactly one word: no spaces, no control characters, letters only.
    assert re.fullmatch(r"[A-Za-z]+", WORD), f"invalid entry word: {WORD!r}"
    assert " " not in WORD and "\n" not in WORD and "\t" not in WORD

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(WORD + "\n")

    # Validate what was actually written.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    assert raw == (WORD + "\n").encode("utf-8"), f"unexpected bytes: {raw!r}"
    text = raw.decode("utf-8")
    words = text.split()
    assert len(words) == 1 and words[0] == WORD, f"not exactly one word: {text!r}"
    print(f"wrote {OUTPUT_PATH}: {WORD!r}")


if __name__ == "__main__":
    main()
