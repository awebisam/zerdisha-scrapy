"""Item processing pipelines for the Zerdisha Scrapers project.

This module implements a series of small, single-responsibility pipelines
that can be chained together for modular, maintainable data processing.
Each pipeline focuses on a specific aspect of data validation and cleaning.

See documentation:
https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""

import logging
import unicodedata
from datetime import datetime
from typing import Any, Union

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from zerdisha_scrapers.items import ArticleItem


class ValidationPipeline:
    """Pipeline for validating essential fields in ArticleItem instances.
    
    This pipeline ensures that all critical fields required for a valid
    article are present and not empty. Missing or empty essential fields
    will cause the item to be dropped with detailed logging.
    
    Essential fields validated:
        - url: The canonical URL of the article
        - title: The article's headline/title  
        - full_text: Complete article content/body text
        - source_name: Name of the news source/publication
    """
    
    def process_item(self, item: ArticleItem, spider: scrapy.Spider) -> ArticleItem:
        """Validate essential fields in the article item.
        
        Args:
            item: The ArticleItem to validate.
            spider: The spider that produced this item.
            
        Returns:
            ArticleItem: The validated item if all essential fields are present.
            
        Raises:
            DropItem: If any essential field is missing or empty.
        """
        adapter = ItemAdapter(item)
        
        # Define essential fields that must be present and non-empty
        essential_fields = ['url', 'title', 'full_text', 'source_name']
        
        for field_name in essential_fields:
            field_value = adapter.get(field_name)
            
            if field_value is None:
                error_msg = f"Missing essential field '{field_name}' in item from {spider.name}"
                spider.logger.warning(error_msg)
                raise DropItem(error_msg)
            
            if isinstance(field_value, str) and not field_value.strip():
                error_msg = f"Empty essential field '{field_name}' in item from {spider.name}"
                spider.logger.warning(error_msg)
                raise DropItem(error_msg)
        
        spider.logger.debug(f"Item validation passed for: {adapter.get('title', 'Unknown')[:50]}...")
        return item


class CleaningPipeline:
    """Pipeline for cleaning and normalizing string fields in ArticleItem instances.
    
    This pipeline performs basic string cleaning operations on all string fields:
    - Strips leading and trailing whitespace
    - Normalizes Unicode to NFC (Normalization Form Composed) for consistency
    
    This ensures consistent string formatting across all articles regardless
    of the source's original formatting or encoding issues.
    """
    
    def process_item(self, item: ArticleItem, spider: scrapy.Spider) -> ArticleItem:
        """Clean and normalize all string fields in the article item.
        
        Args:
            item: The ArticleItem to clean.
            spider: The spider that produced this item.
            
        Returns:
            ArticleItem: The item with cleaned string fields.
        """
        adapter = ItemAdapter(item)
        
        # Process all fields that contain string data
        for field_name, field_value in adapter.items():
            if isinstance(field_value, str):
                # Strip whitespace and normalize Unicode
                cleaned_value = field_value.strip()
                cleaned_value = unicodedata.normalize('NFC', cleaned_value)
                adapter[field_name] = cleaned_value
        
        spider.logger.debug(f"String cleaning completed for: {adapter.get('title', 'Unknown')[:50]}...")
        return item


class TimestampPipeline:
    """Pipeline for handling and standardizing timestamp fields in ArticleItem instances.
    
    This pipeline ensures that date/time fields are properly formatted as
    ISO 8601 strings. It handles various input formats and gracefully
    converts them to the standardized format.
    
    Fields processed:
        - publication_date: When the article was originally published
        - scraped_at: When this article was scraped by our system
    """
    
    def process_item(self, item: ArticleItem, spider: scrapy.Spider) -> ArticleItem:
        """Standardize timestamp fields to ISO 8601 format.
        
        Args:
            item: The ArticleItem to process.
            spider: The spider that produced this item.
            
        Returns:
            ArticleItem: The item with standardized timestamp fields.
        """
        adapter = ItemAdapter(item)
        
        # Process publication_date (optional field)
        publication_date = adapter.get('publication_date')
        if publication_date is not None:
            try:
                standardized_date = self._standardize_timestamp(publication_date)
                adapter['publication_date'] = standardized_date
            except ValueError as e:
                spider.logger.warning(f"Failed to parse publication_date '{publication_date}': {e}")
                # Keep the original value if parsing fails
        
        # Process scraped_at (required field)
        scraped_at = adapter.get('scraped_at')
        if scraped_at is not None:
            try:
                standardized_date = self._standardize_timestamp(scraped_at)
                adapter['scraped_at'] = standardized_date
            except ValueError as e:
                spider.logger.warning(f"Failed to parse scraped_at '{scraped_at}': {e}")
                # Keep the original value if parsing fails
        
        spider.logger.debug(f"Timestamp processing completed for: {adapter.get('title', 'Unknown')[:50]}...")
        return item
    
    def _standardize_timestamp(self, timestamp: Union[str, datetime]) -> str:
        """Convert various timestamp formats to ISO 8601 string.
        
        Args:
            timestamp: The timestamp to standardize (string or datetime object).
            
        Returns:
            str: ISO 8601 formatted timestamp string.
            
        Raises:
            ValueError: If the timestamp cannot be parsed.
        """
        if isinstance(timestamp, datetime):
            return timestamp.isoformat()
        
        if isinstance(timestamp, str):
            # If already in ISO format, validate and return
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                return dt.isoformat()
            except ValueError:
                pass
            
            # Try common date formats
            common_formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%d-%m-%Y',
                '%m-%d-%Y',
            ]
            
            for fmt in common_formats:
                try:
                    dt = datetime.strptime(timestamp, fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            raise ValueError(f"Unable to parse timestamp format: {timestamp}")
        
        raise ValueError(f"Unsupported timestamp type: {type(timestamp)}")


# Legacy pipeline for backward compatibility
class ZerdishaScrapersPipeline:
    """Legacy pipeline for backward compatibility.
    
    This pipeline is kept for compatibility with existing configurations
    but should be replaced with the specific validation, cleaning, and
    timestamp pipelines for new deployments.
    """
    
    def process_item(self, item: ArticleItem, spider: scrapy.Spider) -> ArticleItem:
        """Process item with basic passthrough functionality.
        
        Args:
            item: The item to process.
            spider: The spider that produced this item.
            
        Returns:
            ArticleItem: The unmodified item.
        """
        return item
