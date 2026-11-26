"""Run the entry twice and independently verify its exact output bytes."""

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def check_output(data: bytes) -> str:
    word = data.decode("utf-8", errors="strict")
    if not 1 <= len(word) <= 30:
        raise ValueError("Output must contain 1 to 30 characters.")
    if any(character.isspace() for character in word):
        raise ValueError("Output contains whitespace or a line separator.")
    if not word.isalpha():
        raise ValueError("Output must be exactly one alphabetic word.")
    if data.endswith((b"\n", b"\r")):
        raise ValueError("Output has a trailing newline.")
    return word


def main() -> int:
    repo = Path(__file__).resolve().parent
    verification_root = repo / ".verify"
    try:
        verification_root.mkdir(exist_ok=True)
        outputs = []
        with tempfile.TemporaryDirectory(prefix="check-", dir=verification_root) as tmp:
            for run_number in (1, 2):
                output_dir = Path(tmp) / f"run-{run_number}"
                output_dir.mkdir()
                environment = os.environ.copy()
                environment["OUTPUT_DIR"] = str(output_dir)
                subprocess.run(
                    [sys.executable, str(repo / "main.py")],
                    cwd=repo,
                    env=environment,
                    check=True,
                    capture_output=True,
                    timeout=10,
                )
                data = (output_dir / "entry.txt").read_bytes()
                check_output(data)
                outputs.append(data)
        if outputs[0] != outputs[1]:
            raise ValueError("The two runs produced different bytes.")
        word = check_output(outputs[0])
        print(f"PASS: {word!r}; {len(word)} characters; valid UTF-8; one word;")
        print("PASS: no whitespace or trailing newline; two byte-identical runs.")
        for run_number, data in enumerate(outputs, start=1):
            print(f"Run {run_number} SHA-256: {hashlib.sha256(data).hexdigest()}")
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
