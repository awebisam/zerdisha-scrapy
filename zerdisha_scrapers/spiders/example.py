"""Example spider demonstrating best practices for the Zerdisha Scrapers project.

This spider serves as the gold standard template for all spiders in this project.
It demonstrates proper use of type hints, logging, error handling, and the
ArticleItem data contract.

This spider is for demonstration purposes only and should not be used
to scrape actual websites without permission.
"""

from datetime import datetime, timezone
from typing import Any, Generator, Optional

import scrapy
from scrapy.http import Response

from zerdisha_scrapers.items import ArticleItem


class ExampleSpider(scrapy.Spider):
    """Example spider demonstrating best practices and ArticleItem usage.
    
    This spider serves as a comprehensive template showing:
    - Proper class documentation with Google Style docstrings
    - Strict typing throughout all methods
    - Proper use of self.logger for logging
    - Comprehensive error handling
    - Correct ArticleItem instantiation and population
    - Timezone-aware datetime handling with ISO 8601 serialization
    
    Attributes:
        name: Unique identifier for this spider.
        allowed_domains: List of domains this spider is allowed to crawl.
        start_urls: Initial URLs where the spider begins crawling.
    """
    
    name: str = "example"
    allowed_domains: list[str] = ["example.com"]
    start_urls: list[str] = ["http://example.com"]

    async def start(self) -> None:
        """Generate initial requests for the spider (modern async method).
        
        This method is the modern replacement for start_requests() and supports
        asynchronous execution. It demonstrates proper typing and logging practices.
        """
        self.logger.info(f"Starting {self.name} spider with {len(self.start_urls)} URLs")
        
        for url in self.start_urls:
            self.logger.debug(f"Creating request for URL: {url}")
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"spider_start_time": datetime.now(timezone.utc)}
            )

    def parse(self, response: Response) -> Generator[ArticleItem, None, None]:
        """Parse the main page and extract article data.
        
        This method demonstrates how to properly extract data and populate
        an ArticleItem with all required fields, including proper timezone
        handling and ISO 8601 serialization.
        
        Args:
            response: The HTTP response object containing the page content.
            
        Yields:
            ArticleItem: Populated article item with extracted data.
        """
        self.logger.info(f"Parsing response from {response.url}")
        
        try:
            # Extract article data using CSS selectors
            # Note: These selectors are for demonstration only
            title: Optional[str] = response.css('title::text').get()
            content: Optional[str] = response.css('body::text').get()
            
            if not title:
                self.logger.warning(f"No title found for {response.url}")
                return
            
            if not content:
                self.logger.warning(f"No content found for {response.url}")
                return
            
            # Create timezone-aware timestamps in ISO 8601 format
            scraped_at: str = datetime.now(timezone.utc).isoformat()
            
            # For demonstration, we'll use a placeholder publication date
            # In real spiders, this would be extracted from the page
            publication_date: str = datetime.now(timezone.utc).isoformat()
            
            # Create and populate the ArticleItem
            article: ArticleItem = ArticleItem()
            
            article['url'] = str(response.url)
            article['source_name'] = "Example Domain"
            article['title'] = title.strip()
            article['full_text'] = content.strip()
            article['author'] = "Example Author"  # Would be extracted from page
            article['publication_date'] = publication_date
            article['scraped_at'] = scraped_at
            article['spider_name'] = self.name
            
            self.logger.info(f"Successfully extracted article: {title[:50]}...")
            
            yield article
            
        except Exception as e:
            self.logger.error(f"Error parsing {response.url}: {str(e)}")
            # In production, you might want to yield a failed item or retry
            
    def parse_article(self, response: Response) -> Generator[ArticleItem, None, None]:
        """Parse individual article pages (if following links).
        
        This method would be used when the spider follows links to individual
        article pages. It demonstrates the same patterns as the main parse method.
        
        Args:
            response: The HTTP response object for an individual article page.
            
        Yields:
            ArticleItem: Populated article item with extracted data.
        """
        self.logger.debug(f"Parsing article page: {response.url}")
        
        # Implementation would be similar to parse() method
        # This is a placeholder to demonstrate method structure
        pass
        
    def closed(self, reason: str) -> None:
        """Called when the spider closes.
        
        This method is called when the spider finishes crawling.
        It's useful for cleanup operations and final logging.
        
        Args:
            reason: The reason why the spider was closed.
        """
        self.logger.info(f"Spider {self.name} closed. Reason: {reason}")