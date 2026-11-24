#!/usr/bin/env python3
"""One Word From Your Ex — make.fun entry.

Writes exactly one word to /output/entry.txt: the word an ex would
use to describe the author. Nothing else.
"""

import os
import re

WORD = "placeholder"
OUTPUT_PATH = "/output/entry.txt"


def validate_entry(word: str) -> None:
    """Validate that `word` is exactly one word for the entry.

    Raises AssertionError on any failure: empty, multi-word, non-letters,
    control characters, or over the length bound.
    """
    assert isinstance(word, str), f"entry must be a string: {word!r}"
    assert word, "entry word must not be empty"
    assert len(word) <= 64, f"entry word too long ({len(word)} chars)"
    assert " " not in word and "\n" not in word and "\t" not in word, (
        f"entry word must contain no whitespace: {word!r}"
    )
    assert not any(ord(c) < 32 or ord(c) == 127 for c in word), (
        f"entry word must contain no control characters: {word!r}"
    )
    assert re.fullmatch(r"[A-Za-z]+", word), f"invalid entry word: {word!r}"


def main() -> None:
    validate_entry(WORD)

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


def self_test() -> int:
    """Run validate_entry() against negative cases; exit non-zero on failure."""
    negative_cases = [
        ("", "empty string"),
        ("two words", "two words"),
        ("word1", "word with a digit"),
        ("word ", "word with a trailing space"),
        (" word", "word with a leading space"),
        ("wo\trd", "word with a tab"),
        ("wo\nrd", "word with a newline"),
        ("a" * 65, "word over the length bound"),
    ]
    failures = 0
    for bad, label in negative_cases:
        try:
            validate_entry(bad)
        except AssertionError:
            print(f"self-test ok (rejected): {label}: {bad!r}")
        else:
            failures += 1
            print(f"self-test FAIL (accepted): {label}: {bad!r}")
    # Positive control: the real entry word must pass.
    try:
        validate_entry(WORD)
    except AssertionError as exc:
        failures += 1
        print(f"self-test FAIL (rejected valid word): {exc}")
    else:
        print(f"self-test ok (accepted): valid word {WORD!r}")
    if failures:
        print(f"self-test: {failures} failure(s)")
        return 1
    print(f"self-test: all {len(negative_cases) + 1} cases passed")
    return 0


if __name__ == "__main__":
    import sys

    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    main()
