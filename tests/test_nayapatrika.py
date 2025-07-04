"""Unit tests for the Naya Patrika spider.

This module contains tests for the NayapatrikaSpider class,
focusing on core functionality without complex logger mocking.
"""

import unittest
from unittest.mock import Mock, patch

from zerdisha_scrapers.spiders.nayapatrika import NayapatrikaSpider


class TestNayapatrikaSpider(unittest.TestCase):
    """Test cases for the NayapatrikaSpider class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.spider = NayapatrikaSpider()
    
    def test_spider_attributes(self):
        """Test that spider has correct basic attributes."""
        self.assertEqual(self.spider.name, "nayapatrika")
        self.assertEqual(self.spider.allowed_domains, ["nayapatrikadaily.com"])
        self.assertEqual(self.spider.rss_url, "https://www.nayapatrikadaily.com/?feed=rss2")
    
    @patch('zerdisha_scrapers.spiders.nayapatrika.feedparser.parse')
    def test_start_requests_creates_requests_from_rss_feed(self, mock_feedparser):
        """Test start_requests method creates requests from RSS feed."""
        # Mock RSS feed response
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [
            Mock(
                link="https://www.nayapatrikadaily.com/article1",
                title="Test Article 1"
            ),
            Mock(
                link="https://www.nayapatrikadaily.com/article2", 
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
        self.assertEqual(first_request.url, "https://www.nayapatrikadaily.com/article1")
        self.assertEqual(first_request.callback, self.spider.parse_article)
        self.assertEqual(first_request.meta['rss_title'], "Test Article 1")
        self.assertIn('spider_start_time', first_request.meta)
        
        # Check second request
        second_request = requests[1]
        self.assertEqual(second_request.url, "https://www.nayapatrikadaily.com/article2")
        self.assertEqual(second_request.meta['rss_title'], "Test Article 2")
    
    @patch('zerdisha_scrapers.spiders.nayapatrika.feedparser.parse')
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
    
    @patch('zerdisha_scrapers.spiders.nayapatrika.feedparser.parse')
    def test_start_requests_skips_entries_without_links(self, mock_feedparser):
        """Test start_requests method skips RSS entries without links."""
        # Mock RSS feed with entry missing link
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [
            Mock(title="Test Article 1"),  # Missing link attribute
            Mock(
                link="https://www.nayapatrikadaily.com/article2",
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
        self.assertEqual(requests[0].url, "https://www.nayapatrikadaily.com/article2")
    
    @patch('zerdisha_scrapers.spiders.nayapatrika.feedparser.parse')
    def test_start_requests_handles_feed_parsing_errors(self, mock_feedparser):
        """Test start_requests method handles feedparser errors gracefully."""
        # Mock feedparser to raise an exception
        mock_feedparser.side_effect = Exception("Network error")
        
        # Execute start_requests  
        requests = list(self.spider.start_requests())
        
        # Verify results
        self.assertEqual(len(requests), 0)
    
    def test_extract_publication_date_from_url(self):
        """Test publication date extraction from URL structure."""
        # Mock response with URL containing date
        mock_response = Mock()
        mock_response.url = "https://www.nayapatrikadaily.com/2023/12/25/test-article"
        mock_response.css.return_value.get.return_value = None
        
        # Test date extraction
        result = self.spider._extract_publication_date(mock_response)
        
        # Verify result
        self.assertEqual(result, "2023-12-25")
    
    def test_extract_publication_date_invalid_url(self):
        """Test publication date extraction with invalid URL structure."""
        # Mock response with URL not containing date
        mock_response = Mock()
        mock_response.url = "https://www.nayapatrikadaily.com/category/politics/test-article"
        mock_response.css.return_value.get.return_value = None
        
        # Test date extraction
        result = self.spider._extract_publication_date(mock_response)
        
        # Verify result - should return None for invalid URL
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()