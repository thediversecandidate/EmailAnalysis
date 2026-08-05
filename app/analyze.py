"""Top-level entrypoint tying classification, GenesisAI retrieval, and
draft assembly together. This is the function to call from wherever
emails actually arrive (a real inbox integration is not built -- see
CLAUDE.md)."""

from __future__ import annotations

from dataclasses import dataclass

from app.classify import ClassificationResult, classify
from app.draft import draft_reply
from app.genesisai_client import RetrievedPassage, query_genesisai


@dataclass(frozen=True)
class EmailAnalysisResult:
    classification: ClassificationResult
    passages: list[RetrievedPassage]
    draft: str


def analyze_email(subject: str, body: str) -> EmailAnalysisResult:
    classification = classify(subject, body)
    passages = query_genesisai(f"{subject} {body}", limit=3)
    draft = draft_reply(subject, classification.category, passages)
    return EmailAnalysisResult(classification=classification, passages=passages, draft=draft)
