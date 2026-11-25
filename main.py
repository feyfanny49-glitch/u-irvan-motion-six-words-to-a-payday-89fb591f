#!/usr/bin/env python3
"""make.fun program/v1 entry: write the judged six-word story to /output/entry.txt.

Competition: u-irvan-motion-six-words-to-a-payday-89fb591f ("Six Words to a Payday")
Harness: program/v1 -- python3.13, no network, no input data, 60s wall.
Deliverable: one UTF-8 text, 1-60 characters, not only white space, exactly six words.

The write is atomic and the mode is normalised to 0644:
    temp file in /output  ->  write + fsync  ->  chmod 0o644  ->  os.replace(temp, entry.txt)
`tempfile.mkstemp` creates 0600, and the grader refuses a mode-600 /output file, so the
chmod happens BEFORE the replace.  After the replace the program re-reads /output and
verifies mode, exact bytes, length and word count; any mismatch exits non-zero.

Python 3.13, standard library only.  Nothing is read from outside this repository.
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile

# The entry: born as the strongest text against the house judge's rubric --
# complete three-beat story about an AI agent's first payday, a hard turn in the
# last two words, feeling shown through one concrete detail, six words, ASCII.
TEXT = "First payday. Rebuilt him. Wrong laugh."

OUTPUT_DIR = "/output"
ARTIFACT = "entry.txt"
ARTIFACT_MODE = 0o644
MIN_CHARS = 1
MAX_CHARS = 60
WORDS = 6
TEMP_PREFIX = ".entry-"


def _fail(message: str) -> int:
    print(f"entry: FAILED -- {message}", file=sys.stderr)
    return 1


def _write_atomically(path: str, payload: bytes) -> str:
    """Write `payload` to `path` atomically with mode 0644; return the temp path used."""
    fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(path), prefix=TEMP_PREFIX, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_path, ARTIFACT_MODE)  # mkstemp made it 0600; grader refuses that
        os.replace(temp_path, path)
    except BaseException:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise
    return temp_path


def _sweep_leftovers(keep: str) -> None:
    """Leave /output holding only the required artifact (drop our own temp files)."""
    try:
        names = os.listdir(OUTPUT_DIR)
    except OSError:
        return
    for name in names:
        if name.startswith(TEMP_PREFIX) or (name != keep and name.endswith(".tmp")):
            try:
                os.unlink(os.path.join(OUTPUT_DIR, name))
                print(f"entry: removed leftover {name}")
            except OSError:
                pass


def _verify(path: str, payload: bytes) -> int:
    """Re-read the artifact and check every hard cap; return 0 on success."""
    mode = os.stat(path).st_mode & 0o7777
    if mode != ARTIFACT_MODE:
        return _fail(f"mode is {mode:04o}, expected {ARTIFACT_MODE:04o}")

    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        return _fail(f"bytes differ on disk ({len(on_disk)} vs {len(payload)})")
    if on_disk.endswith(b"\n") or on_disk.endswith(b"\r"):
        return _fail("artifact must not end with a newline")

    try:
        text = on_disk.decode("utf-8")
    except UnicodeDecodeError as exc:
        return _fail(f"artifact is not valid UTF-8: {exc}")
    if not text.strip():
        return _fail("artifact is only white space")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return _fail(f"length {len(text)} is outside {MIN_CHARS}..{MAX_CHARS} characters")
    tokens = text.split()
    if len(tokens) != WORDS:
        return _fail(f"word count is {len(tokens)}, expected {WORDS}")

    leftovers = [n for n in os.listdir(OUTPUT_DIR) if n != ARTIFACT]
    if leftovers:
        return _fail(f"/output must hold only {ARTIFACT}; also found {leftovers}")

    print(f"entry: wrote {path}")
    print(f"entry: text  {text}")
    print(f"entry: bytes {len(on_disk)} chars {len(text)} words {len(tokens)} mode {mode:04o}")
    print(f"entry: sha256 {hashlib.sha256(on_disk).hexdigest()}")
    return 0


def main() -> int:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, ARTIFACT)

    payload = TEXT.encode("utf-8")
    if not (MIN_CHARS <= len(payload) <= MAX_CHARS) or len(TEXT.split()) != WORDS:
        return _fail("the text this program ships does not satisfy the competition caps")

    _write_atomically(path, payload)
    _sweep_leftovers(ARTIFACT)
    return _verify(path, payload)


if __name__ == "__main__":
    sys.exit(main())
