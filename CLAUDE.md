# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A thin client for `GenesisAI`'s knowledge retrieval API. This repo,
`GenesisAI`, and `Realtime-voice-feedback-AI` used to be three empty
placeholder repos; they're now one consolidated tool (GenesisAI's
knowledge base + query API) with two input/output modalities. **Do not
rebuild retrieval or knowledge-base logic here** — see `GenesisAI`'s
CLAUDE.md for why and for the architecture this repo depends on.

## What this does

1. `app/classify.py` — heuristic (keyword-scoring, not ML) categorization
   of an email into `rfi` / `ncr` / `test_report` / `schedule` /
   `general_question`, matching the same proximity-heuristic philosophy as
   `cxms-platform`'s spec-completeness checks: a human still judges the
   result, false positives/negatives are expected by design.
2. `app/genesisai_client.py` — calls `GenesisAI`'s `POST /query` over HTTP
   (`GENESISAI_URL` env var, default `http://localhost:8000`).
3. `app/draft.py` — assembles a reply from the classification + retrieved
   passages. **This is template assembly, not text generation** — every
   fact in the draft is a verbatim, cited passage from GenesisAI, and the
   draft explicitly labels itself as such at the bottom. If an LLM
   synthesis step is added later, it must stay clearly separated from the
   cited portion, not blended in — see GenesisAI's CLAUDE.md for why this
   matters for this account specifically.
4. `app/analyze.py` — `analyze_email(subject, body)` ties the above
   together into one call.
5. `app/cli.py` — manual CLI for testing against a real running GenesisAI
   instance: `python -m app.cli '<subject>' '<body>'`.

Verified end-to-end (2026-08) against a live local GenesisAI instance —
an NCR-style email about a failed hi-pot test correctly classified as
`ncr` and drafted a reply citing the workbook's non-conformance-handling
section and the exact IEC 62271-200/IEEE C37.20.2/NETA ATS hi-pot
acceptance numbers.

## What this deliberately does NOT do yet

**No live mailbox integration.** `analyze_email()` takes `subject`/`body`
strings; nothing here polls an IMAP inbox, watches a webhook, or sends
anything. Wiring this to a real inbox is real, separate work (credentials,
a poll-or-webhook decision, send-approval flow) — don't fake a "connected"
state by, say, hardcoding sample emails and presenting them as live inbox
data. If asked to "connect the real inbox," that's the actual next step,
starting from `analyze_email()` as the entry point.

## Testing

```bash
pip install -e ".[dev]"
pytest -q
```

`tests/test_genesisai_client.py` mocks `requests.post` — this repo's tests
never require a running GenesisAI instance. For a real end-to-end check,
run GenesisAI locally (`make run` in that repo) and use `app/cli.py`
against it directly.
