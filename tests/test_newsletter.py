import pytest
from unittest.mock import patch, Mock, MagicMock
from bs4 import BeautifulSoup
from scrape_substack.newsletter import (
    get_newsletter_post_metadata,
    get_newsletter_recommendations,
    get_post_contents,
    list_all_categories,
    HEADERS,
)


@pytest.fixture
def mock_response():
    response = Mock(ok=True)
    return response


@patch("requests.get")
def test_list_all_categories(mock_get, mock_response):
    return_value = [
        {'id': 96, 'name': 'Culture', 'active': True, 'rank': 0, 'slug': 'culture'}, 
        {'id': 4, 'name': 'Technology', 'active': True, 'rank': 1, 'slug': 'technology'}, 
        {'id': 62, 'name': 'Business', 'active': True, 'rank': 2, 'slug': 'business'}, 
        {'id': 76739, 'name': 'U.S. Politics', 'active': True, 'rank': 3, 'slug': 'us-politics'}, 
        {'id': 153, 'name': 'Finance', 'active': True, 'rank': 4, 'slug': 'finance'}, 
    ]    
    mock_response.json.return_value = return_value
    mock_get.return_value = mock_response
    categories = list_all_categories()
    assert len(categories) == 5
    assert categories == return_value
    

# def test_list_all_categories():
#     categories = list_all_categories()
#     assert len(categories) >= 30
    

@patch("requests.get")
def test_get_newsletter_post_metadata_slugs_only(mock_get, mock_response):
    mock_response.json.return_value = [
        {"id": 1, "slug": "post-1"},
        {"id": 2, "slug": "post-2"},
    ]
    mock_get.return_value = mock_response

    result = get_newsletter_post_metadata("test_subdomain", slugs_only=True)
    assert result == ["post-1", "post-2"]

@patch("requests.get")
def test_get_newsletter_post_metadata_all_metadata(mock_get, mock_response):
    mock_response.json.return_value = [
        {"id": 1, "slug": "post-1", "title": "Post 1"},
        {"id": 2, "slug": "post-2", "title": "Post 2"},
    ]
    mock_get.return_value = mock_response

    result = get_newsletter_post_metadata("test_subdomain", slugs_only=False)
    assert result == [
        {"id": 1, "slug": "post-1", "title": "Post 1"},
        {"id": 2, "slug": "post-2", "title": "Post 2"},
    ]

@patch("requests.get")
def test_get_newsletter_post_metadata_pagination(mock_get):
    mock_get.side_effect = [
        Mock(
            ok=True,
            json=Mock(
                return_value=[
                    {"id": 1, "slug": "post-1"},
                    {"id": 2, "slug": "post-2"},
                ]
            ),
        ),
        Mock(
            ok=True,
            json=Mock(
                return_value=[
                    {"id": 3, "slug": "post-3"},
                    {"id": 4, "slug": "post-4"},
                ]
            ),
        ),
    ]

    result = get_newsletter_post_metadata(
        "test_subdomain", slugs_only=True, start_offset=0, end_offset=20
    )
    assert result == ["post-1", "post-2", "post-3", "post-4"]

@patch("requests.get")
def test_get_newsletter_post_metadata_no_posts(mock_get, mock_response):
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    result = get_newsletter_post_metadata("test_subdomain")
    assert result == []

@pytest.fixture
def mock_bs_components():
    mock_div = MagicMock()
    mock_div.find.return_value = {"href": "https://mocked_url.com?param=value"}
    return mock_div

@patch("requests.get")
@patch.object(BeautifulSoup, "find_all")
@patch.object(BeautifulSoup, "__init__", return_value=None)
def test_get_newsletter_recommendations(
    mock_bs_init, mock_find_all, mock_get, mock_response, mock_bs_components
):
    mock_response.text = "mocked_html"
    mock_get.return_value = mock_response

    mock_find_all.side_effect = [
        [mock_bs_components, mock_bs_components],  # div_elements
        [Mock(text="title1"), Mock(text="title2")],  # titles
    ]

    result = get_newsletter_recommendations("test_subdomain")

    assert result == [
        {"title": "title1", "url": "https://mocked_url.com"},
        {"title": "title2", "url": "https://mocked_url.com"},
    ]

    mock_get.assert_called_once_with(
        "https://test_subdomain.substack.com/recommendations",
        headers=HEADERS,
        timeout=30,
    )
    mock_bs_init.assert_called_once_with("mocked_html", "html.parser")
    assert mock_find_all.call_count == 2

@patch("requests.get")
def test_get_post_contents_html_only(mock_get, mock_response):
    mock_response.json.return_value = {
        "body_html": "<html><body>Test post</body></html>"
    }
    mock_get.return_value = mock_response

    result = get_post_contents("test_subdomain", "test_slug", html_only=True)
    assert result == "<html><body>Test post</body></html>"

@patch("requests.get")
def test_get_post_contents_all_metadata(mock_get, mock_response):
    mock_response.json.return_value = {
        "body_html": "<html><body>Test post</body></html>",
        "title": "Test post",
        "author": "Test author",
        "date": "2022-01-01",
    }
    mock_get.return_value = mock_response

    result = get_post_contents("test_subdomain", "test_slug", html_only=False)
    assert result == {
        "body_html": "<html><body>Test post</body></html>",
        "title": "Test post",
        "author": "Test author",
        "date": "2022-01-01",
    }
