"""Generate the fixed Grandma entry using only the Python standard library."""

from pathlib import Path
import os


ENTRY_WORD: str = "ChattyPT"


def validate_word(word: str) -> None:
    """Accept only one to thirty letters, with no whitespace."""
    length = len(word)
    if length < 1 or length > 30:
        raise ValueError("Entry length must be between 1 and 30 characters.")
    for letter in word:
        if letter.isspace():
            raise ValueError("Whitespace is not allowed in the entry.")
    if not word.isalpha():
        raise ValueError("The entry must be a single word containing only letters.")


def main() -> None:
    """Validate the constant and write its exact UTF-8 bytes to entry.txt."""
    validate_word(ENTRY_WORD)
    payload = ENTRY_WORD.encode("utf-8")
    destination = Path(os.environ.get("OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    entry_path = destination / "entry.txt"
    entry_path.write_bytes(payload)


if __name__ == "__main__":
    main()
