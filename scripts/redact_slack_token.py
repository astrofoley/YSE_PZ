#!/usr/bin/env python3
"""Rewrite files in the working tree to remove a leaked Slack bot token."""
import re
from pathlib import Path

SECRET = ""
REPLACEMENT = 'SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")'
PATTERN = re.compile(
    r'SLACK_BOT_TOKEN\s*=\s*["\']' + re.escape(SECRET) + r'["\']'
)


def main():
    root = Path(".")
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue
        if SECRET not in text:
            continue
        new_text = PATTERN.sub(REPLACEMENT, text)
        new_text = new_text.replace(SECRET, "")
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"redacted: {path}")


if __name__ == "__main__":
    main()
