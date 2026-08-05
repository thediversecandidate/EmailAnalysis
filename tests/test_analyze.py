from unittest.mock import patch

from app.analyze import analyze_email
from app.classify import Category
from app.genesisai_client import RetrievedPassage


def test_analyze_email_ties_classification_and_draft_together():
    fake_passages = [RetrievedPassage("workbook.md", "b", "h", "Relevant fact.", 5.0)]
    with patch("app.analyze.query_genesisai", return_value=fake_passages) as mock_query:
        result = analyze_email("RFI: chiller voltage", "Please confirm the design voltage.")

    assert result.classification.category == Category.RFI
    assert result.passages == fake_passages
    assert "Relevant fact." in result.draft
    mock_query.assert_called_once_with("RFI: chiller voltage Please confirm the design voltage.", limit=3)
