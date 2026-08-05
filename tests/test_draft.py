from app.classify import Category
from app.draft import draft_reply
from app.genesisai_client import RetrievedPassage


def test_draft_includes_all_cited_passages():
    passages = [
        RetrievedPassage("workbook.md", "Section 5 > 5.2 Hi-Pot", "5.2 Hi-Pot", "Hi-pot pushes voltage above normal operating levels.", 12.0),
        RetrievedPassage("workbook.md", "Section 5 > 5.3 Megger", "5.3 Megger", "Insulation resistance testing verifies dielectric integrity.", 9.0),
    ]
    draft = draft_reply("Hi-pot test question", Category.TEST_REPORT, passages)

    assert "workbook.md" in draft
    assert "Hi-pot pushes voltage above normal operating levels." in draft
    assert "Insulation resistance testing verifies dielectric integrity." in draft
    assert "Section 5 > 5.2 Hi-Pot" in draft


def test_draft_labels_itself_as_not_ai_generated():
    draft = draft_reply("Subject", Category.GENERAL_QUESTION, [])
    assert "not an AI-written response" in draft


def test_draft_handles_no_passages_found():
    draft = draft_reply("Obscure question", Category.GENERAL_QUESTION, [])
    assert "needs a human answer" in draft


def test_draft_truncates_long_passages():
    long_text = "x" * 1000
    passages = [RetrievedPassage("f.md", "b", "h", long_text, 1.0)]
    draft = draft_reply("Subject", Category.RFI, passages)
    assert "..." in draft
    assert long_text not in draft


def test_draft_uses_category_specific_opening():
    ncr_draft = draft_reply("Subject", Category.NCR, [])
    rfi_draft = draft_reply("Subject", Category.RFI, [])
    assert "non-conformance" in ncr_draft.lower()
    assert "rfi" in rfi_draft.lower()
