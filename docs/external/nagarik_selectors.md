## Nagarik News

### Article Title
- CSS: `h1.title`
- XPath: `//h1[@class='title']`
- Notes: The main article title is consistently found within an `h1` tag with the class `title`.

### Full Article Text
- CSS: `.content-wrapper p`
- XPath: `//div[@class='content-wrapper']//p`
- Notes: The main article content is typically within `<p>` tags nested inside a `div` with the class `content-wrapper`. Some articles might have additional formatting (e.g., `<strong>`, `<em>`) within these paragraphs.

### Author Name
- CSS: `.author-name` or `span.author`
- XPath: `//span[@class='author-name']` or `//span[@class='author']`
- Notes: Author names are often within `span` tags with classes like `author-name` or `author`. This can vary.

### Publication Date
- CSS: `.date` or `time`
- XPath: `//span[@class='date']` or `//time`
- Notes: Dates are usually within `span` tags with class `date` or `time` tags. The format is typically Nepali, so conversion to ISO 8601 will be necessary. Look for `datetime` attribute in `time` tag for ISO format.

### Article URL
- Canonical URL: Look for `<link rel="canonical" href="...">` in the HTML head.
- Notes: The article URL is the current page URL. Canonical URLs are usually present in the `<head>` section.

### Tags or Categories
- CSS: `.tags a`
- XPath: `//div[@class='tags']//a`
- Notes: Tags or categories are often found within `<a>` tags inside a `div` with the class `tags`.

### Navigation and Date Filtering
- Nagarik News uses a clear URL structure for articles, including the date. Example: `https://nagariknews.nagariknetwork.com/politics/1481501-1751559076.html`. The numbers in the URL might correspond to article IDs or timestamps. Further investigation is needed to determine if date-based navigation is possible through URL manipulation or if archive pages are available. The publication date on the article page can be used for filtering after extraction.

