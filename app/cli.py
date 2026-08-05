"""Manual CLI for testing analyze_email() against a real GenesisAI
instance. Not a mailbox integration -- see CLAUDE.md for why."""

import sys

from app.analyze import analyze_email
from app.genesisai_client import GenesisAIError


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python -m app.cli '<subject>' '<body>'", file=sys.stderr)
        sys.exit(1)

    subject, body = sys.argv[1], sys.argv[2]
    try:
        result = analyze_email(subject, body)
    except GenesisAIError as exc:
        print(f"Error: {exc}\nIs GenesisAI running (GENESISAI_URL, default http://localhost:8000)?", file=sys.stderr)
        sys.exit(1)

    print(f"Category: {result.classification.category.value}")
    print(f"Matched keywords: {', '.join(result.classification.matched_keywords) or '(none)'}")
    print()
    print(result.draft)


if __name__ == "__main__":
    main()
