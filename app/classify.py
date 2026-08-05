"""Heuristic email categorization for data-center construction /
commissioning consulting correspondence.

Keyword-scoring, not ML/NLP -- the same proximity-heuristic philosophy as
cxms-platform's app/spec_checks/checklist.py (a human still judges the
result; false positives/negatives are expected by design). No training
data exists for this account's actual email traffic, so a classifier that
claimed to be more than that would be overclaiming, not more capable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Category(str, Enum):
    RFI = "rfi"
    NCR = "ncr"
    TEST_REPORT = "test_report"
    SCHEDULE = "schedule"
    GENERAL_QUESTION = "general_question"


_PATTERNS: dict[Category, tuple[re.Pattern, ...]] = {
    Category.RFI: (
        re.compile(r"\bRFI\b"),
        re.compile(r"request for information", re.IGNORECASE),
        re.compile(r"please (confirm|advise|clarify)", re.IGNORECASE),
    ),
    Category.NCR: (
        re.compile(r"\bNCR\b"),
        re.compile(r"non-?conformance", re.IGNORECASE),
        re.compile(r"\bdeficienc(y|ies)\b", re.IGNORECASE),
        re.compile(r"punch\s*list", re.IGNORECASE),
        re.compile(r"does not (meet|comply with) spec", re.IGNORECASE),
    ),
    Category.TEST_REPORT: (
        re.compile(r"\b(IST|FPT)\b"),
        re.compile(r"functional performance test", re.IGNORECASE),
        re.compile(r"\bhi-?pot\b", re.IGNORECASE),
        re.compile(r"\bmegger\b", re.IGNORECASE),
        re.compile(r"acceptance test", re.IGNORECASE),
        re.compile(r"test (result|report)s?", re.IGNORECASE),
    ),
    Category.SCHEDULE: (
        re.compile(r"\bschedule\b", re.IGNORECASE),
        re.compile(r"\bdelay(ed|s)?\b", re.IGNORECASE),
        re.compile(r"\bmilestone\b", re.IGNORECASE),
        re.compile(r"behind schedule", re.IGNORECASE),
        re.compile(r"critical path", re.IGNORECASE),
    ),
}


@dataclass(frozen=True)
class ClassificationResult:
    category: Category
    matched_keywords: tuple[str, ...]


def classify(subject: str, body: str) -> ClassificationResult:
    text = f"{subject}\n{body}"

    best_category = Category.GENERAL_QUESTION
    best_matches: tuple[str, ...] = ()

    for category, patterns in _PATTERNS.items():
        matches = tuple(m.group(0) for p in patterns if (m := p.search(text)))
        if len(matches) > len(best_matches):
            best_category = category
            best_matches = matches

    return ClassificationResult(category=best_category, matched_keywords=best_matches)
