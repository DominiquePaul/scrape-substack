import pytest
from unittest.mock import patch, Mock
from scrape_substack.user import (
    get_user_id,
    get_user_reads,
    get_user_likes,
    get_user_notes,
)


@pytest.fixture
def mock_response():
    return Mock(ok=True)


@patch("requests.get")
def test_get_user_id(mock_get, mock_response):
    mock_response.json.return_value = {"id": 123}
    mock_get.return_value = mock_response

    result = get_user_id("testuser")
    assert result == 123


@patch("requests.get")
def test_get_user_reads(mock_get, mock_response):
    mock_response.json.return_value = {
        "subscriptions": [
            {
                "publication": {"id": "123", "name": "Test Publication"},
                "membership_state": "subscribed",
            }
        ]
    }
    mock_get.return_value = mock_response

    expected_result = [
        {
            "publication_id": "123",
            "publication_name": "Test Publication",
            "subscription_status": "subscribed",
        }
    ]
    result = get_user_reads("testuser")
    assert result == expected_result


@patch("requests.get")
def test_get_user_likes(mock_get, mock_response):
    mock_response.json.return_value = {"items": ["post1", "post2"]}
    mock_get.return_value = mock_response

    result = get_user_likes(123)
    assert result == ["post1", "post2"]


@patch("requests.get")
def test_get_user_notes(mock_get, mock_response):
    mock_response.json.return_value = {"items": ["note1", "note2"]}
    mock_get.return_value = mock_response

    result = get_user_notes(123)
    assert result == ["note1", "note2"]
