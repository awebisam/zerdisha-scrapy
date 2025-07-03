"""Hybrid RSS/Scrapy spider for The Kathmandu Post.

This spider implements a hybrid data ingestion strategy combining RSS feed
discovery with full article content extraction. It uses The Kathmandu Post's
RSS feed for efficient article discovery and then fetches complete article
content from individual pages using Scrapy.

The spider demonstrates:
- RSS feed parsing using feedparser
- Hybrid approach: RSS for discovery, Scrapy for content extraction
- Proper use of type hints, logging, and error handling
- ArticleItem data contract compliance
- Timezone-aware datetime handling with ISO 8601 serialization
"""

import re
from datetime import datetime, timezone
from typing import Any, Generator, Optional

import feedparser
import scrapy
from scrapy.http import Request, Response

from zerdisha_scrapers.items import ArticleItem


class KathmandupostSpider(scrapy.Spider):
    """Hybrid RSS/Scrapy spider for The Kathmandu Post news articles.

    This spider uses The Kathmandu Post's RSS feed to discover new articles
    and then scrapes the full content from individual article pages. It
    demonstrates the hybrid approach combining efficient RSS-based discovery
    with comprehensive content extraction.

    The spider follows all project coding standards including:
    - Strict typing throughout all methods
    - Comprehensive error handling and logging
    - Proper ArticleItem instantiation and population
    - Timezone-aware datetime handling

    Attributes:
        name: Unique identifier for this spider.
        allowed_domains: List of domains this spider is allowed to crawl.
        rss_url: The RSS feed URL for article discovery.
    """

    name: str = "kathmandupost"
    allowed_domains: list[str] = ["kathmandupost.com"]
    rss_url: str = "https://kathmandupost.com/rss"

    def start_requests(self) -> Generator[Request, None, None]:
        """Generate initial requests by parsing the RSS feed.

        This method fetches and parses The Kathmandu Post's RSS feed to
        discover new articles. For each article found in the feed, it
        creates a request to the full article page with metadata preserved.

        Yields:
            Request: Scrapy requests for individual article pages with
                    RSS metadata passed via the meta parameter.
        """
        self.logger.info(
            f"Starting {self.name} spider with RSS feed: {self.rss_url}")

        try:
            # Parse the RSS feed using feedparser
            self.logger.debug(f"Fetching RSS feed from: {self.rss_url}")
            feed = feedparser.parse(self.rss_url)

            if feed.bozo:
                self.logger.warning(
                    f"RSS feed parsing had issues: {feed.bozo_exception}")

            # Check if we got any entries
            if not hasattr(feed, 'entries') or not feed.entries:
                self.logger.error(
                    f"No entries found in RSS feed: {self.rss_url}")
                return

            self.logger.info(f"Found {len(feed.entries)} articles in RSS feed")

            # Create requests for each article in the feed
            for entry in feed.entries:
                if not hasattr(entry, 'link') or not entry.link:
                    self.logger.warning("RSS entry missing link, skipping")
                    continue

                # Extract metadata from RSS entry
                article_url: str = str(entry.link)
                title: str = getattr(entry, 'title', '')

                self.logger.debug(
                    f"Creating request for article: {title[:50]}...")

                # Yield request to the full article page
                yield scrapy.Request(
                    url=article_url,
                    callback=self.parse_article,
                    meta={
                        'rss_title': title,
                        'spider_start_time': datetime.now(timezone.utc)
                    }
                )

        except Exception as e:
            self.logger.error(
                f"Error processing RSS feed {self.rss_url}: {str(e)}")

    def parse_article(self, response: Response) -> Generator[ArticleItem, None, None]:
        """Parse individual article pages and extract full content.

        This method extracts the complete article content from individual
        article pages using CSS selectors. It combines the content with
        metadata from the RSS feed to create a complete ArticleItem.

        Args:
            response: The HTTP response object for an individual article page.

        Yields:
            ArticleItem: Populated article item with extracted data and
                        RSS metadata.
        """
        self.logger.debug(f"Parsing article page: {response.url}")

        try:
            # Extract full article content using CSS selector
            paragraphs: list[str] = response.css('main p::text').getall()

            if not paragraphs:
                self.logger.warning(
                    f"No content found using CSS selector 'main p' for {response.url}")
                return

            # Join all paragraphs into full text
            full_text: str = '\n\n'.join(
                paragraph.strip() for paragraph in paragraphs if paragraph.strip())

            if not full_text:
                self.logger.warning(
                    f"No meaningful content extracted from {response.url}")
                return

            # Get metadata from RSS feed (passed via meta)
            rss_title: str = response.meta.get('rss_title', '')

            # Use RSS title if available, otherwise try to extract from page
            title: str = rss_title
            if not title:
                page_title: Optional[str] = response.css('h1::text').get()
                title = page_title.strip() if page_title else ''

            if not title:
                self.logger.warning(f"No title found for {response.url}")
                return

            # Extract author if available (optional field)
            author: Optional[str] = response.css('.article-author::text').get()
            if author:
                author = author.strip()

            # Extract publication date from the article page
            publication_date: Optional[str] = self._extract_publication_date(
                response)

            # Create timezone-aware timestamps in ISO 8601 format
            scraped_at: str = datetime.now(timezone.utc).isoformat()

            # Create and populate the ArticleItem
            article: ArticleItem = ArticleItem()

            article['url'] = str(response.url)
            article['source_name'] = "The Kathmandu Post"
            article['title'] = title.strip()
            article['full_text'] = full_text
            article['author'] = author
            article['publication_date'] = publication_date
            article['scraped_at'] = scraped_at
            article['spider_name'] = self.name

            self.logger.info(
                f"Successfully extracted article: {title[:50]}...")

            yield article

        except Exception as e:
            self.logger.error(
                f"Error parsing article {response.url}: {str(e)}")

    def _extract_publication_date(self, response: Response) -> Optional[str]:
        """Extract publication date from the article page.

        This method attempts to extract the publication date from various
        sources on the article page, with fallback to URL parsing if needed.

        Args:
            response: The HTTP response object for an individual article page.

        Returns:
            The publication date in ISO 8601 format, or None if not found.
        """
        try:
            # Try to extract from "Published at" text on the page
            published_text: Optional[str] = response.css(
                '.updated-time:contains("Published at") ::text').get()

            if published_text:
                # Clean up the text and extract the date part
                # Example: "Published at : July 3, 2025"
                published_text = published_text.strip()
                if "Published at" in published_text:
                    date_part = published_text.split("Published at")[1].strip()
                    if date_part.startswith(":"):
                        date_part = date_part[1:].strip()

                    # Try to parse the date and convert to ISO format
                    try:
                        # Handle format like "July 3, 2025"
                        parsed_date = datetime.strptime(date_part, "%B %d, %Y")
                        return parsed_date.isoformat()
                    except ValueError:
                        self.logger.debug(
                            f"Could not parse published date: {date_part}")

            # Fallback: Extract date from URL structure
            # URL format: https://kathmandupost.com/category/YYYY/MM/DD/article-slug
            url_parts = response.url.split('/')
            if len(url_parts) >= 6:
                try:
                    year = url_parts[4]
                    month = url_parts[5]
                    day = url_parts[6]

                    # Validate that these are actually date components
                    if (year.isdigit() and len(year) == 4 and
                        month.isdigit() and len(month) == 2 and
                            day.isdigit() and len(day) == 2):

                        # Create ISO date string
                        date_str = f"{year}-{month}-{day}"
                        # Validate the date by parsing it
                        datetime.strptime(date_str, "%Y-%m-%d")
                        return date_str

                except (ValueError, IndexError):
                    self.logger.debug(
                        f"Could not extract date from URL: {response.url}")

            self.logger.warning(
                f"No publication date found for {response.url}")
            return None

        except Exception as e:
            self.logger.error(
                f"Error extracting publication date from {response.url}: {str(e)}")
            return None

    def closed(self, reason: str) -> None:
        """Called when the spider closes.

        This method is called when the spider finishes crawling.
        It provides final logging and cleanup operations.

        Args:
            reason: The reason why the spider was closed.
        """
        self.logger.info(f"Spider {self.name} closed. Reason: {reason}")
