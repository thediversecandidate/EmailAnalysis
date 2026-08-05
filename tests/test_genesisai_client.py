from unittest.mock import MagicMock, patch

import pytest
import requests

from app.genesisai_client import GenesisAIError, query_genesisai


def _mock_response(json_data, status_code=200):
    resp = MagicMock()
    resp.json.return_value = json_data
    resp.status_code = status_code
    if status_code >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(f"{status_code} error")
    else:
        resp.raise_for_status.side_effect = None
    return resp


def test_query_genesisai_returns_passages():
    payload = {
        "question": "hi-pot",
        "results": [
            {"source_file": "workbook.md", "breadcrumb": "b", "heading": "h", "text": "t", "score": 1.0}
        ],
    }
    with patch("app.genesisai_client.requests.post", return_value=_mock_response(payload)) as mock_post:
        results = query_genesisai("hi-pot testing", limit=3, base_url="http://fake-genesisai")

    assert len(results) == 1
    assert results[0].source_file == "workbook.md"
    mock_post.assert_called_once()
    call_kwargs = mock_post.call_args
    assert call_kwargs.args[0] == "http://fake-genesisai/query"
    assert call_kwargs.kwargs["json"] == {"question": "hi-pot testing", "limit": 3}


def test_query_genesisai_wraps_connection_errors():
    with patch("app.genesisai_client.requests.post", side_effect=requests.ConnectionError("refused")):
        with pytest.raises(GenesisAIError):
            query_genesisai("anything", base_url="http://unreachable")


def test_query_genesisai_wraps_http_errors():
    with patch("app.genesisai_client.requests.post", return_value=_mock_response({}, status_code=503)):
        with pytest.raises(GenesisAIError):
            query_genesisai("anything", base_url="http://fake-genesisai")
