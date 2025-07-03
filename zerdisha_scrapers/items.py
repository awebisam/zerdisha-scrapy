"""Item definitions for the Zerdisha Scrapers project.

This module defines the data contracts used by spiders to structure
and validate scraped data. All items follow strict typing conventions
and include comprehensive field documentation.

See documentation:
https://docs.scrapy.org/en/latest/topics/items.html
"""

from datetime import datetime
from typing import Optional

import scrapy


class ArticleItem(scrapy.Item):
    """Core data structure for news articles scraped from various sources.

    This item represents a standardized format for all news articles
    collected by the Zerdisha data ingestion system. It ensures consistent
    data structure across different news sources and spiders.

    All date fields are timezone-aware and serialized as ISO 8601 strings
    to maintain consistency and enable proper temporal analysis.

    Fields:
        url: The canonical URL of the article.
        source_name: Name of the news source/publication.
        title: The article's headline/title.
        full_text: Complete article content/body text.
        author: Article author name(s).
        publication_date: When the article was originally published (ISO 8601).
        scraped_at: When this article was scraped by our system (ISO 8601).
        spider_name: Name of the spider that collected this article.
    """

    # Article identification and source
    url = scrapy.Field(
        serializer=str,
        doc="The canonical URL where this article was found"
    )

    source_name = scrapy.Field(
        serializer=str,
        doc="Name of the news source or publication (e.g., 'BBC News', 'Reuters')"
    )

    # Article content
    title = scrapy.Field(
        serializer=str,
        doc="The article's headline or title"
    )

    full_text = scrapy.Field(
        serializer=str,
        doc="Complete article body text, cleaned of HTML and formatting"
    )

    author = scrapy.Field(
        serializer=str,
        doc="Article author name(s), if available"
    )

    # Temporal information (timezone-aware, ISO 8601 format)
    publication_date = scrapy.Field(
        serializer=str,
        doc="Original publication date as ISO 8601 string (timezone-aware)"
    )

    scraped_at = scrapy.Field(
        serializer=str,
        doc="Timestamp when this article was scraped as ISO 8601 string (timezone-aware)"
    )

    # Metadata
    spider_name = scrapy.Field(
        serializer=str,
        doc="Name of the spider that collected this article"
    )
