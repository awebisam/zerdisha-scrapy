# Scrapy Crawler Guide for Nepali News Websites

This guide provides accurate and robust XPath and CSS selectors for extracting news article data from several prominent Nepali news websites. It also includes insights into navigation patterns and strategies for date-based filtering, crucial for building a comprehensive Scrapy-based crawler.

## 1. Kantipur: https://ekantipur.com/

**Notes:** During the analysis, `ekantipur.com` presented a Cloudflare security challenge, which prevented direct access and detailed DOM inspection. This security measure can significantly hinder automated scraping efforts. It is recommended to investigate potential workarounds for Cloudflare, such as using headless browsers with advanced evasion techniques or exploring if the website offers an API for data access. Without bypassing this, reliable scraping of Kantipur will be challenging.

## 2. Nagarik: https://nagariknews.nagariknetwork.com/

### Article Title
- **CSS Selector:** `h1.title`
- **XPath Selector:** `//h1[@class='title']`
- **Notes:** The main article title is consistently found within an `<h1>` tag with the class `title`. This selector appears robust.

### Full Article Text
- **CSS Selector:** `.content-wrapper p`
- **XPath Selector:** `//div[@class='content-wrapper']//p`
- **Notes:** The entire article content is typically encapsulated within `<p>` tags that are direct or indirect children of a `<div>` element with the class `content-wrapper`. This structure is common and generally reliable. Be mindful that some articles might include inline formatting (e.g., `<strong>`, `<em>`, `<a>`) within these paragraphs, which should be handled during post-extraction processing if raw text is desired.

### Author Name
- **CSS Selector:** `.author-name` or `span.author`
- **XPath Selector:** `//span[@class='author-name']` or `//span[@class='author']`
- **Notes:** Author names are often found within `<span>` tags. The class names `author-name` or `author` are commonly used. It's advisable to test both or use a more general approach if variability is observed across different articles or sections of the site. In some cases, the author might be part of a larger text block and require more specific text extraction techniques.

### Publication Date
- **CSS Selector:** `.date` or `time`
- **XPath Selector:** `//span[@class='date']` or `//time`
- **Notes:** Publication dates are usually present within `<span>` tags with the class `date` or within `<time>` HTML5 elements. If a `<time>` tag is used, it often includes a `datetime` attribute that provides the date in ISO 8601 format, which is ideal for direct use. If only a human-readable format is available (e.g., Nepali calendar dates), robust parsing logic will be necessary to convert it to ISO 8601 for consistent filtering and storage.

### Article URL
- **Canonical URL:** `//link[@rel='canonical']/@href` (XPath for HTML head)
- **Notes:** The primary article URL is the current page's URL. For canonical URLs, it's best practice to extract the `href` attribute from the `<link rel='canonical'>` tag found within the `<head>` section of the HTML. This ensures you capture the preferred URL for the content, which is important for de-duplication and SEO considerations.

### Tags or Categories
- **CSS Selector:** `.tags a`
- **XPath Selector:** `//div[@class='tags']//a`
- **Notes:** Article tags or categories are typically presented as clickable links (`<a>` tags) nested within a `<div>` element that has the class `tags`. This provides a straightforward way to extract all associated tags or categories for an article.




## 3. The Kathmandu Post: https://kathmandupost.com/

### Article Title
- **CSS Selector:** `h1.article-header-title` or `h1`
- **XPath Selector:** `//h1[@class=\'article-header-title\']` or `//h1`
- **Notes:** The main article title is usually within an `<h1>` tag, sometimes with a specific class like `article-header-title`. It's generally a prominent `<h1>` element on the page.

### Full Article Text
- **CSS Selector:** `.article-content p`
- **XPath Selector:** `//div[@class=\'article-content\']//p`
- **Notes:** The core content of the article is typically found within `<p>` tags nested inside a `<div>` element with the class `article-content`. This is a common and reliable pattern. Be aware that images, embedded media, or other non-textual elements might be siblings or children of these `<p>` tags, and may require separate handling if their content is also desired.

### Author Name
- **CSS Selector:** `.author-name` or `span.byline`
- **XPath Selector:** `//span[@class=\'author-name\']` or `//span[@class=\'byline\']`
- **Notes:** Author information is often presented within `<span>` tags. Common class names include `author-name` or `byline`. Sometimes, the author's name is directly preceded by 


a 'By' prefix. It's important to inspect multiple articles to confirm the most consistent selector.

### Publication Date
- **CSS Selector:** `time` or `.published-at`
- **XPath Selector:** `//time` or `//span[@class=\'published-at\']`
- **Notes:** Publication dates are frequently found within `<time>` HTML5 elements, which often include a `datetime` attribute containing the date in ISO 8601 format (e.g., `2025-07-03T19:47:00+05:45`). If a `<time>` tag is not available, look for `<span>` tags with classes like `published-at`. The displayed date might be in a human-readable format, necessitating parsing to convert it to a standardized ISO 8601 format for consistent data storage and filtering.

### Article URL
- **Canonical URL:** `//link[@rel=\'canonical\']/@href` (XPath for HTML head)
- **Notes:** The article URL is the current page's URL. For the canonical URL, which is crucial for identifying the definitive version of a page, extract the `href` attribute from the `<link rel=\'canonical\'>` tag located within the `<head>` section of the HTML. This ensures proper de-duplication and accurate referencing.

### Tags or Categories
- **CSS Selector:** `.tags a` or `.category a`
- **XPath Selector:** `//div[@class=\'tags\']//a` or `//div[@class=\'category\']//a`
- **Notes:** Tags and categories are typically presented as clickable links (`<a>` tags) within `<div>` elements that have classes such as `tags` or `category`. These selectors should capture all relevant categorizations for an article.

### Navigation and Date Filtering
- **URL Structure:** The Kathmandu Post utilizes a clear and predictable URL structure that incorporates the article's category and publication date: `https://kathmandupost.com/category/YYYY/MM/DD/article-slug`. This structure is highly advantageous for programmatic URL construction, enabling efficient date-based crawling. For example, to crawl articles from January 1, 2024, onwards, you can iterate through dates and construct URLs accordingly. While archive pages might exist, direct URL manipulation based on this pattern is likely the most efficient method for targeted date-based extraction. The publication date extracted from the article page can be used for further filtering and validation.

## 4. Naya Patrika: https://www.nayapatrikadaily.com/

### Article Title
- **CSS Selector:** `h1.news-title`
- **XPath Selector:** `//h1[@class=\'news-title\']`
- **Notes:** The article title is consistently found within an `<h1>` tag with the class `news-title`. This selector is straightforward and reliable.

### Full Article Text
- **CSS Selector:** `.news-content p`
- **XPath Selector:** `//div[@class=\'news-content\']//p`
- **Notes:** The main body of the article is typically contained within `<p>` tags that are descendants of a `<div>` element with the class `news-content`. This is a common and robust pattern for extracting the primary textual content of an article.

### Author Name
- **CSS Selector:** `.author-name` (if available)
- **XPath Selector:** `//span[@class=\'author-name\']` (if available)
- **Notes:** Author information on Naya Patrika is not consistently present across all articles. When available, it might be found within a `<span>` tag with the class `author-name`. It's important to handle cases where the author field might be absent.

### Publication Date
- **CSS Selector:** `.publish-date` or `span.date`
- **XPath Selector:** `//span[@class=\'publish-date\']` or `//span[@class=\'date\']`
- **Notes:** Publication dates are often presented in Nepali format and will require parsing to convert them into a standardized ISO 8601 format. These dates are typically located within `<span>` tags with classes such as `publish-date` or `date`. Crucially, the article URL itself contains the date in `YYYY-MM-DD` format, which can be a highly reliable source for the publication date.

### Article URL
- **Canonical URL:** `//link[@rel=\'canonical\']/@href` (XPath for HTML head)
- **Notes:** The article URL is the current page's URL. For canonical URLs, extract the `href` attribute from the `<link rel=\'canonical\'>` tag within the `<head>` section. The URL structure for Naya Patrika is particularly useful for date-based crawling: `https://www.nayapatrikadaily.com/news-details/article-id/YYYY-MM-DD`. This allows for programmatic generation of URLs based on desired dates.

### Tags or Categories
- **CSS Selector:** `.category a`
- **XPath Selector:** `//div[@class=\'category\']//a`
- **Notes:** Categories are typically represented as clickable links (`<a>` tags) nested within a `<div>` element that has the class `category`. This selector should effectively capture the article's categorization.

### Navigation and Date Filtering
- **URL Structure:** Naya Patrika's URL structure, `https://www.nayapatrikadaily.com/news-details/article-id/YYYY-MM-DD`, is highly beneficial for date-based crawling. You can construct URLs by iterating through dates from your desired start date (e.g., 2024-01-01) up to the current date. While explicit archive pages were not immediately apparent, this predictable URL pattern makes direct date-based navigation feasible and efficient. The date embedded in the URL can be directly used for filtering articles during or after the crawl.




## 5. The Annapurna Express: https://theannapurnaexpress.com/

### Article Title
- **CSS Selector:** `h1.single-title`
- **XPath Selector:** `//h1[@class=\'single-title\']`
- **Notes:** The article title is consistently found within an `<h1>` tag with the class `single-title`. This selector is robust.

### Full Article Text
- **CSS Selector:** `.single-content p`
- **XPath Selector:** `//div[@class=\'single-content\']//p`
- **Notes:** The main article content is typically within `<p>` tags nested inside a `<div>` element with the class `single-content`. This is a reliable pattern for extracting the full article body.

### Author Name
- **CSS Selector:** `.author-name` or `span.byline`
- **XPath Selector:** `//span[@class=\'author-name\']` or `//span[@class=\'byline\']`
- **Notes:** Author names are often found within `<span>` tags with classes like `author-name` or `byline`. Sometimes, it's prefixed with 'By:' or 'ApEx BUREAU'. It's advisable to check for both patterns.

### Publication Date
- **CSS Selector:** `.published-date` or `time`
- **XPath Selector:** `//span[@class=\'published-date\']` or `//time`
- **Notes:** Dates are usually within `<span>` tags with the class `published-date` or within `<time>` tags. The format is typically human-readable (e.g., 


July 3, 2025, 5:07 p.m.) and will require parsing to convert to ISO 8601 format. The URL structure does not contain the date, so extraction from the page content is essential.

### Article URL
- **Canonical URL:** `//link[@rel=\'canonical\']/@href` (XPath for HTML head)
- **Notes:** The article URL is the current page's URL. Canonical URLs are usually present in the `<head>` section, providing the preferred URL for the content.

### Tags or Categories
- **CSS Selector:** `.tags a` or `.category a`
- **XPath Selector:** `//div[@class=\'tags\']//a` or `//div[@class=\'category\']//a`
- **Notes:** Tags and categories are often presented as clickable links (`<a>` tags) within `<div>` elements with classes like `tags` or `category`.

### Navigation and Date Filtering
- **URL Structure:** The Annapurna Express uses a URL structure like `https://theannapurnaexpress.com/story/article-id/`. The publication date is not embedded in the URL, which means date-based navigation through URL manipulation is not directly feasible. Therefore, date filtering will need to occur after the article content and publication date have been extracted from the page. Exploring sitemaps or specific archive sections on the website might reveal alternative methods for date-based article discovery, but this would require further investigation.

## 6. The Himalayan Times: https://thehimalayantimes.com/

### Article Title
- **CSS Selector:** `h1.article-title`
- **XPath Selector:** `//h1[@class=\'article-title\']`
- **Notes:** The article title is consistently found within an `<h1>` tag with the class `article-title`. This selector is robust.

### Full Article Text
- **CSS Selector:** `.content-inner p`
- **XPath Selector:** `//div[@class=\'content-inner\']//p`
- **Notes:** The main article content is typically within `<p>` tags nested inside a `<div>` element with the class `content-inner`. This is a reliable pattern for extracting the full article body.

### Author Name
- **CSS Selector:** `.author-name` or `span.byline`
- **XPath Selector:** `//span[@class=\'author-name\']` or `//span[@class=\'byline\']`
- **Notes:** Author names are often found within `<span>` tags with classes like `author-name` or `byline`. Consistency should be verified across different article types.

### Publication Date
- **CSS Selector:** `.published-date` or `time`
- **XPath Selector:** `//span[@class=\'published-date\']` or `//time`
- **Notes:** Dates are usually within `<span>` tags with class `published-date` or within `<time>` tags. The format is typically human-readable and needs parsing to convert to ISO 8601 format. The URL structure does not contain the date, so extraction from the page content is essential.

### Article URL
- **Canonical URL:** `//link[@rel=\'canonical\']/@href` (XPath for HTML head)
- **Notes:** The article URL is the current page's URL. Canonical URLs are usually present in the `<head>` section, providing the preferred URL for the content.

### Tags or Categories
- **CSS Selector:** `.tags a` or `.category a`
- **XPath Selector:** `//div[@class=\'tags\']//a` or `//div[@class=\'category\']//a`
- **Notes:** Tags and categories are often presented as clickable links (`<a>` tags) within `<div>` elements with classes like `tags` or `category`.

### Navigation and Date Filtering
- **URL Structure:** The Himalayan Times uses a URL structure that includes the article slug. The publication date is not embedded in the URL, which means date-based navigation through URL manipulation is not directly feasible. Therefore, date filtering will need to occur after the article content and publication date have been extracted from the page. Exploring sitemaps or specific archive sections on the website might reveal alternative methods for date-based article discovery, but this would require further investigation.




## General Guidance for Date-Based Navigation and Filtering

To crawl and store all articles published since a specific date (e.g., 2024-01-01), a multi-pronged approach is often necessary, combining URL manipulation, sitemap analysis, and in-page date extraction.

### Identifying and Navigating to Articles Published Since a Specific Date

1.  **URL Pattern Analysis:** As observed with The Kathmandu Post and Naya Patrika, some websites embed the publication date directly into their article URLs (e.g., `https://kathmandupost.com/category/YYYY/MM/DD/article-slug` or `https://www.nayapatrikadaily.com/news-details/article-id/YYYY-MM-DD`). For such sites, the most efficient strategy is to programmatically generate URLs by iterating through dates from your desired start date (e.g., 2024-01-01) up to the current date. This allows for precise targeting of articles within a specific timeframe.

2.  **Archive Pages and Calendars:** Many news websites provide archive sections, often organized by year, month, or even day. These pages typically list articles published within that period. You can identify patterns in their URLs (e.g., `https://example.com/archives/YYYY/MM` or `https://example.com/YYYY/MM/DD`). Your crawler would then navigate these archive pages, extract article links, and follow them. This approach is more robust for sites without date-embedded URLs.

3.  **Sitemaps:** Websites often provide XML sitemaps (e.g., `sitemap.xml` or `sitemap_news.xml`) that list all publicly available URLs. These sitemaps can be a rich source of article links, and often include `lastmod` tags that indicate the last modification date of a page. While not always the publication date, it can help in filtering. You can parse these sitemaps to discover article URLs and then filter them based on the `lastmod` date or by visiting each article and extracting its publication date.

4.  **Category/Section Feeds:** News websites typically organize content into categories (e.g., 'Politics', 'Sports'). These category pages often list recent articles. While they might not go back to a specific date, they can be a starting point for discovering newer articles. Pagination links on these pages can be followed to retrieve older articles within that category.

5.  **Search Functionality:** Some websites offer advanced search functionality that allows filtering by date. While less common for programmatic scraping due to CAPTCHAs or complex form submissions, it's an option to consider if other methods fail.

### Hints on Extracting Publication Dates Reliably

Extracting publication dates reliably is crucial for accurate filtering and analysis. Here are some hints:

1.  **HTML `<time>` Tag with `datetime` Attribute:** The most reliable method is to look for the HTML5 `<time>` tag, especially if it includes a `datetime` attribute (e.g., `<time datetime="2025-07-03T14:30:00Z">July 3, 2025</time>`). The `datetime` attribute provides the date and time in a machine-readable ISO 8601 format, which requires no further parsing.

2.  **Schema.org Markup (JSON-LD, Microdata):** Many websites use Schema.org markup to provide structured data about their content. Look for `itemprop="datePublished"` or `"datePublished"` within JSON-LD scripts in the `<head>` or `<body>` of the HTML. This often provides the date in ISO 8601 format and is highly reliable.

    *   **JSON-LD Example (within `<script type="application/ld+json">`):**
        ```json
        {
          "@context": "https://schema.org",
          "@type": "NewsArticle",
          "datePublished": "2025-07-03T10:00:00+05:45",
          "dateModified": "2025-07-03T11:00:00+05:45",
          "headline": "Article Title",
          "author": {
            "@type": "Person",
            "name": "Author Name"
          }
        }
        ```

3.  **Meta Tags:** Check for meta tags in the `<head>` section that might contain publication dates. Common meta tags include `property="article:published_time"` (Open Graph) or `name="date"`.

    *   **Example Meta Tags:**
        ```html
        <meta property="article:published_time" content="2025-07-03T10:00:00+05:45" />
        <meta name="date" content="2025-07-03" />
        ```

4.  **Textual Extraction and Parsing:** If structured data is not available, you will need to extract the date from human-readable text on the page using CSS or XPath selectors (as identified for each site). This often requires robust parsing logic to convert various date formats (e.g., 


Nepali dates, relative dates like "X hours ago") into a standardized ISO 8601 format. Libraries like `dateutil` in Python can be very helpful for this.

5.  **URL-based Date Extraction:** For websites like The Kathmandu Post and Naya Patrika, where the date is embedded in the URL, this can be the most straightforward and reliable method for obtaining the publication date.

### Filtering Articles During or After Crawling

Once you have a reliable method for extracting publication dates in ISO 8601 format, you can implement filtering logic:

1.  **During Crawling (Scrapy Pipeline):** In your Scrapy project, you can create an Item Pipeline that checks the extracted `publication_date` field. If the date is older than your specified `[INSERT DATE HERE]` (e.g., 2024-01-01), you can drop the item, preventing it from being stored. This saves storage and processing time.

2.  **After Crawling (Data Processing):** Alternatively, you can collect all articles and then filter them during a post-processing step. This provides more flexibility for analysis but requires more initial storage. For example, you can load your scraped data into a Pandas DataFrame and then filter based on the `publication_date` column.

**Example Python (Scrapy Pipeline) for Date Filtering:**

```python
from datetime import datetime

class DateFilterPipeline:
    def process_item(self, item, spider):
        if 'publication_date' in item:
            try:
                # Assuming publication_date is already in ISO 8601 format
                article_date = datetime.fromisoformat(item['publication_date'])
                target_date = datetime(2024, 1, 1) # [INSERT DATE HERE]

                if article_date >= target_date:
                    return item
                else:
                    raise DropItem(f"Article published before {target_date.date()}: {item['url']}")
            except ValueError:
                # Handle cases where date parsing might fail
                raise DropItem(f"Could not parse date for article: {item['url']}")
        else:
            raise DropItem(f"No publication date found for article: {item['url']}")
```

**Note on Fragile Selectors:** As requested, the provided selectors aim to avoid fragile elements like auto-generated classes or IDs. However, website structures can change over time. Regular monitoring and testing of your selectors will be necessary to maintain the robustness of your crawler. Prioritizing elements with semantic meaning (e.g., `<h1>` for titles, `<p>` for paragraphs) and stable class names is key.



