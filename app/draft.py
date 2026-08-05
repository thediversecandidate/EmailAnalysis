"""Assemble a draft reply from a classified email + retrieved passages.

This is template assembly, not text generation -- no LLM writes any of
the prose here. Every fact in the draft is a verbatim, cited passage from
GenesisAI. Keep it that way: if this ever grows an LLM synthesis step,
label the generated portion explicitly and separately from the cited
portion, per GenesisAI's CLAUDE.md.
"""

from __future__ import annotations

from app.classify import Category
from app.genesisai_client import RetrievedPassage

_OPENING = {
    Category.RFI: "Thanks for the RFI. Here's what our reference material says:",
    Category.NCR: "Acknowledging the reported non-conformance. Relevant acceptance criteria:",
    Category.TEST_REPORT: "Thanks for sending the test results. Relevant standard(s) for review:",
    Category.SCHEDULE: "Noted on the schedule update. Related reference material:",
    Category.GENERAL_QUESTION: "Thanks for the question. Here's what we found in our reference material:",
}

_CLOSING = {
    Category.RFI: "Let us know if this doesn't fully answer the question and we'll follow up with the design team.",
    Category.NCR: "Please confirm corrective action once complete so we can close this out.",
    Category.TEST_REPORT: "We'll compare these results against the cited acceptance criteria and follow up.",
    Category.SCHEDULE: "We'll factor this into the commissioning schedule and follow up on next steps.",
    Category.GENERAL_QUESTION: "Let us know if you need more detail on any of this.",
}


def draft_reply(subject: str, category: Category, passages: list[RetrievedPassage]) -> str:
    lines = [f"Subject: RE: {subject}", "", _OPENING[category], ""]

    if not passages:
        lines.append("(No matching reference material found -- this needs a human answer, not a template.)")
    else:
        for i, p in enumerate(passages, start=1):
            lines.append(f"{i}. {p.breadcrumb} ({p.source_file})")
            snippet = p.text.strip().replace("\n", " ")
            if len(snippet) > 400:
                snippet = snippet[:400].rstrip() + "..."
            lines.append(f'   "{snippet}"')
            lines.append("")

    lines.append(_CLOSING[category])
    lines.append("")
    lines.append("-- Draft assembled from GenesisAI's knowledge base. Review before sending;")
    lines.append("   this is templated, cited reference material, not an AI-written response.")

    return "\n".join(lines)
