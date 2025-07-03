"""Unit tests for the Annapurna Express spider.

This module contains tests for the AnnapurnaSpider class,
focusing on core functionality without complex logger mocking.
"""

import unittest
from unittest.mock import Mock, patch

from scrapy.http import HtmlResponse, Request
from zerdisha_scrapers.spiders.annapurna import AnnapurnaSpider


class TestAnnapurnaSpider(unittest.TestCase):
    """Test cases for the AnnapurnaSpider class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.spider = AnnapurnaSpider()
    
    def test_spider_attributes(self):
        """Test that spider has correct basic attributes."""
        self.assertEqual(self.spider.name, "annapurna")
        self.assertEqual(self.spider.allowed_domains, ["theannapurnaexpress.com"])
        self.assertEqual(self.spider.rss_url, "https://theannapurnaexpress.com/feed")
    
    @patch('zerdisha_scrapers.spiders.annapurna.feedparser.parse')
    def test_start_requests_creates_requests_from_rss_feed(self, mock_feedparser):
        """Test start_requests method creates requests from RSS feed."""
        # Mock RSS feed response
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [
            Mock(
                link="https://theannapurnaexpress.com/article1",
                title="Test Article 1"
            ),
            Mock(
                link="https://theannapurnaexpress.com/article2", 
                title="Test Article 2"
            )
        ]
        mock_feedparser.return_value = mock_feed
        
        # Execute start_requests
        requests = list(self.spider.start_requests())
        
        # Verify results
        self.assertEqual(len(requests), 2)
        
        # Check first request
        first_request = requests[0]
        self.assertEqual(first_request.url, "https://theannapurnaexpress.com/article1")
        self.assertEqual(first_request.callback, self.spider.parse_article)
        self.assertEqual(first_request.meta['rss_title'], "Test Article 1")
        self.assertIn('spider_start_time', first_request.meta)
        
        # Check second request
        second_request = requests[1]
        self.assertEqual(second_request.url, "https://theannapurnaexpress.com/article2")
        self.assertEqual(second_request.meta['rss_title'], "Test Article 2")
    
    @patch('zerdisha_scrapers.spiders.annapurna.feedparser.parse')
    def test_start_requests_handles_empty_rss_feed(self, mock_feedparser):
        """Test start_requests method handles empty RSS feed."""
        # Mock empty RSS feed response
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = []
        mock_feedparser.return_value = mock_feed
        
        # Execute start_requests
        requests = list(self.spider.start_requests())
        
        # Verify results
        self.assertEqual(len(requests), 0)
    
    @patch('zerdisha_scrapers.spiders.annapurna.feedparser.parse')
    def test_start_requests_skips_entries_without_links(self, mock_feedparser):
        """Test start_requests method skips RSS entries without links."""
        # Mock RSS feed with entry missing link
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [
            Mock(title="Test Article 1"),  # Missing link attribute
            Mock(
                link="https://theannapurnaexpress.com/article2",
                title="Test Article 2"
            )
        ]
        # Remove link attribute from first entry
        del mock_feed.entries[0].link
        mock_feedparser.return_value = mock_feed
        
        # Execute start_requests
        requests = list(self.spider.start_requests())
        
        # Verify results - should skip entry without link
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, "https://theannapurnaexpress.com/article2")

    def test_parse_article_extracts_content_successfully(self):
        """Test parse_article method extracts content using correct selector."""
        # Create mock HTML response
        html_content = """
        <html>
            <body>
                <h1>Test Article Title</h1>
                <div class="single-content">
                    <p>This is the first paragraph of the article.</p>
                    <p>This is the second paragraph with more content.</p>
                    <p>And this is the final paragraph.</p>
                </div>
            </body>
        </html>
        """
        
        # Create mock response with meta data
        response = HtmlResponse(
            url="https://theannapurnaexpress.com/test-article",
            body=html_content,
            encoding='utf-8'
        )
        
        # Create a request with meta and assign to response
        request = Request(
            url="https://theannapurnaexpress.com/test-article",
            meta={
                'rss_title': 'Test Article from RSS',
                'spider_start_time': '2023-01-01T00:00:00+00:00'
            }
        )
        response.request = request
        
        # Execute parse_article
        articles = list(self.spider.parse_article(response))
        
        # Verify results
        self.assertEqual(len(articles), 1)
        
        article = articles[0]
        self.assertEqual(article['url'], "https://theannapurnaexpress.com/test-article")
        self.assertEqual(article['source_name'], "The Annapurna Express")
        self.assertEqual(article['title'], "Test Article from RSS")
        self.assertEqual(article['spider_name'], "annapurna")
        
        expected_text = "This is the first paragraph of the article.\n\nThis is the second paragraph with more content.\n\nAnd this is the final paragraph."
        self.assertEqual(article['full_text'], expected_text)

    def test_parse_article_handles_missing_content(self):
        """Test parse_article method handles pages without content gracefully."""
        # Create mock HTML response without the expected content
        html_content = """
        <html>
            <body>
                <h1>Test Article Title</h1>
                <div class="different-class">
                    <p>This content won't be found by our selector.</p>
                </div>
            </body>
        </html>
        """
        
        # Create mock response with meta data
        response = HtmlResponse(
            url="https://theannapurnaexpress.com/test-article",
            body=html_content,
            encoding='utf-8'
        )
        
        # Create a request with meta and assign to response
        request = Request(
            url="https://theannapurnaexpress.com/test-article",
            meta={
                'rss_title': 'Test Article from RSS',
                'spider_start_time': '2023-01-01T00:00:00+00:00'
            }
        )
        response.request = request
        
        # Execute parse_article
        articles = list(self.spider.parse_article(response))
        
        # Verify results - should return empty because no content found
        self.assertEqual(len(articles), 0)

    def test_extract_publication_date_from_meta_tag(self):
        """Test publication date extraction from meta tags."""
        # Create mock HTML response with meta tag
        html_content = """
        <html>
            <head>
                <meta property="article:published_time" content="2023-01-01T12:00:00Z" />
            </head>
            <body>
                <div class="single-content">
                    <p>Test content</p>
                </div>
            </body>
        </html>
        """
        
        response = HtmlResponse(
            url="https://theannapurnaexpress.com/test-article",
            body=html_content,
            encoding='utf-8'
        )
        
        # Test the private method
        publication_date = self.spider._extract_publication_date(response)
        self.assertIsNotNone(publication_date)
        self.assertIn("2023-01-01", publication_date)

    def test_extract_publication_date_from_url(self):
        """Test publication date extraction from URL structure."""
        response = HtmlResponse(
            url="https://theannapurnaexpress.com/news/2023/12/25/test-article",
            body="<html><body><p>Test</p></body></html>",
            encoding='utf-8'
        )
        
        # Test the private method  
        publication_date = self.spider._extract_publication_date(response)
        self.assertEqual(publication_date, "2023-12-25")


if __name__ == '__main__':
    unittest.main()