## Naya Patrika

### Article Title
- CSS: `h1.news-title`
- XPath: `//h1[@class=\'news-title\\]`
- Notes: The article title is within an `h1` tag with the class `news-title`.

### Full Article Text
- CSS: `.news-content p`
- XPath: `//div[@class=\'news-content\\]//p`
- Notes: The main article content is within `<p>` tags inside a `div` with the class `news-content`.

### Author Name
- CSS: `.author-name` (if available)
- XPath: `//span[@class=\'author-name\\]` (if available)
- Notes: Author information is not consistently available on all articles. When present, it might be in a `span` with class `author-name`.

### Publication Date
- CSS: `.publish-date` or `span.date`
- XPath: `//span[@class=\'publish-date\\]` or `//span[@class=\'date\\]`
- Notes: Dates are often in Nepali format and need parsing. They are usually within `span` tags with classes like `publish-date` or `date`. The URL also contains the date in `YYYY-MM-DD` format.

### Article URL
- Canonical URL: Look for `<link rel="canonical" href="...">` in the HTML head.
- Notes: The article URL is the current page URL. Canonical URLs are usually present in the `<head>` section. The URL structure includes the date: `https://www.nayapatrikadaily.com/news-details/article-id/YYYY-MM-DD`.

### Tags or Categories
- CSS: `.category a`
- XPath: `//div[@class=\'category\\]//a`
- Notes: Categories are typically links within a `div` with the class `category`.

### Navigation and Date Filtering
- Naya Patrika uses a URL structure that includes the date: `https://www.nayapatrikadaily.com/news-details/article-id/YYYY-MM-DD`. This allows for programmatic generation of URLs for date-based crawling. The date in the URL can be used for filtering. Archive pages are not immediately apparent, but the URL structure is very helpful.

