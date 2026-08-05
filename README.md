# EmailAnalysis

A thin client for `GenesisAI`: classifies inbound commissioning/data-center
construction correspondence (RFI, NCR, test report, schedule, general
question) and drafts a reply built from cited passages GenesisAI retrieves.
See `CLAUDE.md` for how this fits with `GenesisAI` and
`Realtime-voice-feedback-AI`.

## Quick start

```bash
pip install -e ".[dev]"
pytest -q
# with a GenesisAI instance running (default http://localhost:8000):
python -m app.cli "NCR-14: Switchgear hi-pot failure" \
  "During acceptance testing the bus hi-pot test failed on Bay 3. Please advise on next steps."
```

Not a live mailbox integration — see `CLAUDE.md`.
