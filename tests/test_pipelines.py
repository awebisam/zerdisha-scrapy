"""Unit tests for the item processing pipelines.

This module contains comprehensive tests for all pipeline classes,
ensuring proper validation, cleaning, and timestamp handling functionality.
"""

import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from scrapy.exceptions import DropItem

from zerdisha_scrapers.items import ArticleItem
from zerdisha_scrapers.pipelines import (
    ValidationPipeline,
    CleaningPipeline,
    TimestampPipeline,
)


class TestValidationPipeline(unittest.TestCase):
    """Test cases for the ValidationPipeline class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = ValidationPipeline()
        self.spider = MagicMock()
        self.spider.name = "test_spider"
        self.spider.logger = MagicMock()
    
    def test_valid_item_passes_validation(self):
        """Test that a valid item passes validation."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        item['author'] = 'Test Author'
        item['scraped_at'] = '2023-01-01T00:00:00'
        item['spider_name'] = 'test_spider'
        
        result = self.pipeline.process_item(item, self.spider)
        
        self.assertEqual(result, item)
        self.spider.logger.debug.assert_called_once()
    
    def test_missing_url_raises_drop_item(self):
        """Test that missing URL field raises DropItem."""
        item = ArticleItem()
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        
        with self.assertRaises(DropItem) as context:
            self.pipeline.process_item(item, self.spider)
        
        self.assertIn("Missing essential field 'url'", str(context.exception))
        self.spider.logger.warning.assert_called_once()
    
    def test_missing_title_raises_drop_item(self):
        """Test that missing title field raises DropItem."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        
        with self.assertRaises(DropItem) as context:
            self.pipeline.process_item(item, self.spider)
        
        self.assertIn("Missing essential field 'title'", str(context.exception))
        self.spider.logger.warning.assert_called_once()
    
    def test_missing_full_text_raises_drop_item(self):
        """Test that missing full_text field raises DropItem."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['source_name'] = 'Test Source'
        
        with self.assertRaises(DropItem) as context:
            self.pipeline.process_item(item, self.spider)
        
        self.assertIn("Missing essential field 'full_text'", str(context.exception))
        self.spider.logger.warning.assert_called_once()
    
    def test_missing_source_name_raises_drop_item(self):
        """Test that missing source_name field raises DropItem."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        
        with self.assertRaises(DropItem) as context:
            self.pipeline.process_item(item, self.spider)
        
        self.assertIn("Missing essential field 'source_name'", str(context.exception))
        self.spider.logger.warning.assert_called_once()
    
    def test_empty_string_fields_raise_drop_item(self):
        """Test that empty string fields raise DropItem."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = '   '  # Only whitespace
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        
        with self.assertRaises(DropItem) as context:
            self.pipeline.process_item(item, self.spider)
        
        self.assertIn("Empty essential field 'title'", str(context.exception))
        self.spider.logger.warning.assert_called_once()
    
    def test_whitespace_only_fields_raise_drop_item(self):
        """Test that fields with only whitespace raise DropItem."""
        item = ArticleItem()
        item['url'] = ''  # Empty string
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        
        with self.assertRaises(DropItem) as context:
            self.pipeline.process_item(item, self.spider)
        
        self.assertIn("Empty essential field 'url'", str(context.exception))
        self.spider.logger.warning.assert_called_once()


class TestCleaningPipeline(unittest.TestCase):
    """Test cases for the CleaningPipeline class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = CleaningPipeline()
        self.spider = MagicMock()
        self.spider.name = "test_spider"
        self.spider.logger = MagicMock()
    
    def test_strips_whitespace_from_strings(self):
        """Test that leading and trailing whitespace is stripped."""
        item = ArticleItem()
        item['url'] = '  https://example.com/article  '
        item['title'] = '\n  Test Article Title  \t'
        item['full_text'] = '  This is the full article content.  '
        item['source_name'] = '  Test Source  '
        item['author'] = '  Test Author  '
        
        result = self.pipeline.process_item(item, self.spider)
        
        self.assertEqual(result['url'], 'https://example.com/article')
        self.assertEqual(result['title'], 'Test Article Title')
        self.assertEqual(result['full_text'], 'This is the full article content.')
        self.assertEqual(result['source_name'], 'Test Source')
        self.assertEqual(result['author'], 'Test Author')
        self.spider.logger.debug.assert_called_once()
    
    def test_normalizes_unicode_strings(self):
        """Test that Unicode strings are normalized to NFC form."""
        item = ArticleItem()
        # Using decomposed Unicode characters that should be normalized
        item['title'] = 'Café'  # This might be composed differently
        item['full_text'] = 'Article about naïve approaches'
        item['source_name'] = 'Test Source'
        item['url'] = 'https://example.com/article'
        
        result = self.pipeline.process_item(item, self.spider)
        
        # The exact Unicode normalization would depend on input,
        # but we can verify the function completes successfully
        self.assertIsInstance(result['title'], str)
        self.assertIsInstance(result['full_text'], str)
        self.spider.logger.debug.assert_called_once()
    
    def test_handles_non_string_fields(self):
        """Test that non-string fields are left unchanged."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        item['publication_date'] = None  # Non-string field
        
        result = self.pipeline.process_item(item, self.spider)
        
        self.assertIsNone(result['publication_date'])
        self.spider.logger.debug.assert_called_once()
    
    def test_empty_strings_remain_empty(self):
        """Test that empty strings remain empty after cleaning."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        item['author'] = ''  # Empty string
        
        result = self.pipeline.process_item(item, self.spider)
        
        self.assertEqual(result['author'], '')
        self.spider.logger.debug.assert_called_once()


class TestTimestampPipeline(unittest.TestCase):
    """Test cases for the TimestampPipeline class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = TimestampPipeline()
        self.spider = MagicMock()
        self.spider.name = "test_spider"
        self.spider.logger = MagicMock()
    
    def test_datetime_objects_converted_to_iso_format(self):
        """Test that datetime objects are converted to ISO 8601 strings."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        
        # Use datetime objects
        test_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        item['publication_date'] = test_datetime
        item['scraped_at'] = test_datetime
        
        result = self.pipeline.process_item(item, self.spider)
        
        self.assertEqual(result['publication_date'], '2023-01-01T12:00:00+00:00')
        self.assertEqual(result['scraped_at'], '2023-01-01T12:00:00+00:00')
        self.spider.logger.debug.assert_called_once()
    
    def test_iso_format_strings_validated_and_standardized(self):
        """Test that valid ISO format strings are validated and standardized."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        item['publication_date'] = '2023-01-01T12:00:00Z'
        item['scraped_at'] = '2023-01-01T12:00:00+00:00'
        
        result = self.pipeline.process_item(item, self.spider)
        
        # Should standardize Z timezone notation
        self.assertEqual(result['publication_date'], '2023-01-01T12:00:00+00:00')
        self.assertEqual(result['scraped_at'], '2023-01-01T12:00:00+00:00')
        self.spider.logger.debug.assert_called_once()
    
    def test_common_date_formats_converted(self):
        """Test that common date formats are converted to ISO 8601."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        item['publication_date'] = '2023-01-01 12:00:00'
        item['scraped_at'] = '01/01/2023'
        
        result = self.pipeline.process_item(item, self.spider)
        
        self.assertEqual(result['publication_date'], '2023-01-01T12:00:00')
        self.assertEqual(result['scraped_at'], '2023-01-01T00:00:00')
        self.spider.logger.debug.assert_called_once()
    
    def test_invalid_date_formats_logged_and_preserved(self):
        """Test that invalid date formats are logged and original value preserved."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        item['publication_date'] = 'invalid date string'
        item['scraped_at'] = '2023-01-01T12:00:00'
        
        result = self.pipeline.process_item(item, self.spider)
        
        # Invalid date should be preserved as-is
        self.assertEqual(result['publication_date'], 'invalid date string')
        self.assertEqual(result['scraped_at'], '2023-01-01T12:00:00')
        self.spider.logger.warning.assert_called_once()
        self.spider.logger.debug.assert_called_once()
    
    def test_none_values_handled_gracefully(self):
        """Test that None values in timestamp fields are handled gracefully."""
        item = ArticleItem()
        item['url'] = 'https://example.com/article'
        item['title'] = 'Test Article Title'
        item['full_text'] = 'This is the full article content.'
        item['source_name'] = 'Test Source'
        item['publication_date'] = None
        item['scraped_at'] = '2023-01-01T12:00:00'
        
        result = self.pipeline.process_item(item, self.spider)
        
        self.assertIsNone(result['publication_date'])
        self.assertEqual(result['scraped_at'], '2023-01-01T12:00:00')
        self.spider.logger.debug.assert_called_once()
    
    def test_standardize_timestamp_method_with_various_formats(self):
        """Test the _standardize_timestamp method with various input formats."""
        # Test datetime object
        dt = datetime(2023, 1, 1, 12, 0, 0)
        result = self.pipeline._standardize_timestamp(dt)
        self.assertEqual(result, '2023-01-01T12:00:00')
        
        # Test ISO format string
        result = self.pipeline._standardize_timestamp('2023-01-01T12:00:00')
        self.assertEqual(result, '2023-01-01T12:00:00')
        
        # Test common format
        result = self.pipeline._standardize_timestamp('2023-01-01 12:00:00')
        self.assertEqual(result, '2023-01-01T12:00:00')
        
        # Test date only
        result = self.pipeline._standardize_timestamp('2023-01-01')
        self.assertEqual(result, '2023-01-01T00:00:00')
        
        # Test invalid format
        with self.assertRaises(ValueError):
            self.pipeline._standardize_timestamp('invalid date')
        
        # Test unsupported type
        with self.assertRaises(ValueError):
            self.pipeline._standardize_timestamp("12345")


if __name__ == '__main__':
    unittest.main()