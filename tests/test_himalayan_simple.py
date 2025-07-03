"""Unit tests for the Himalayan Times spider.

This module contains tests for the HimalayanSpider class,
focusing on core functionality without complex logger mocking.
"""

import unittest
from unittest.mock import Mock, patch

from zerdisha_scrapers.spiders.himalayan import HimalayanSpider


class TestHimalayanSpider(unittest.TestCase):
    """Test cases for the HimalayanSpider class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.spider = HimalayanSpider()
    
    def test_spider_attributes(self):
        """Test that spider has correct basic attributes."""
        self.assertEqual(self.spider.name, "himalayan")
        self.assertEqual(self.spider.allowed_domains, ["thehimalayantimes.com"])
        self.assertEqual(self.spider.rss_url, "https://thehimalayantimes.com/feed")
    
    @patch('zerdisha_scrapers.spiders.himalayan.feedparser.parse')
    def test_start_requests_creates_requests_from_rss_feed(self, mock_feedparser):
        """Test start_requests method creates requests from RSS feed."""
        # Mock RSS feed response with two articles
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [
            Mock(
                link="https://thehimalayantimes.com/article1",
                title="Test Article 1"
            ),
            Mock(
                link="https://thehimalayantimes.com/article2",
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
        self.assertEqual(first_request.url, "https://thehimalayantimes.com/article1")
        self.assertEqual(first_request.callback, self.spider.parse_article)
        self.assertEqual(first_request.meta['rss_title'], "Test Article 1")
        self.assertIn('spider_start_time', first_request.meta)
        
        # Check second request
        second_request = requests[1]
        self.assertEqual(second_request.url, "https://thehimalayantimes.com/article2")
        self.assertEqual(second_request.meta['rss_title'], "Test Article 2")
    
    @patch('zerdisha_scrapers.spiders.himalayan.feedparser.parse')
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
    
    @patch('zerdisha_scrapers.spiders.himalayan.feedparser.parse')
    def test_start_requests_skips_entries_without_links(self, mock_feedparser):
        """Test start_requests method skips RSS entries without links."""
        # Mock RSS feed with entry missing link
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [
            Mock(title="Test Article 1"),  # Missing link attribute
            Mock(
                link="https://thehimalayantimes.com/article2",
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
        self.assertEqual(requests[0].url, "https://thehimalayantimes.com/article2")


if __name__ == '__main__':
    unittest.main()