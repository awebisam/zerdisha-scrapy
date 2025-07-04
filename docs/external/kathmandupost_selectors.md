## The Kathmandu Post

### Article Title
- CSS: `h1.article-header-title` or `h1`
- XPath: `//h1[@class=\'article-header-title\']` or `//h1`
- Notes: The main article title is usually within an `h1` tag, sometimes with a specific class like `article-header-title`.

### Full Article Text
- CSS: `.article-content p`
- XPath: `//div[@class=\'article-content\']//p`
- Notes: The article content is typically within `<p>` tags inside a `div` with the class `article-content`. Be aware of nested elements like `<strong>` or `<a>` within paragraphs.

### Author Name
- CSS: `.author-name` or `span.byline`
- XPath: `//span[@class=\'author-name\']` or `//span[@class=\'byline\']`
- Notes: Author names are often found within `span` tags with classes like `author-name` or `byline`. Sometimes it's directly under a 'By' prefix.

### Publication Date
- CSS: `time` or `.published-at`
- XPath: `//time` or `//span[@class=\'published-at\']`
- Notes: Publication dates are often within `<time>` tags with a `datetime` attribute for ISO 8601 format, or within `span` tags with a class like `published-at`. The format on the page might be human-readable and require parsing.

### Article URL
- Canonical URL: Look for `<link rel="canonical" href="...">` in the HTML head.
- Notes: The article URL is the current page URL. Canonical URLs are usually present in the `<head>` section.

### Tags or Categories
- CSS: `.tags a` or `.category a`
- XPath: `//div[@class=\'tags\']//a` or `//div[@class=\'category\']//a`
- Notes: Tags and categories are often links within `div` elements with classes like `tags` or `category`.

### Navigation and Date Filtering
- The Kathmandu Post uses a clear URL structure that includes the category and date: `https://kathmandupost.com/category/YYYY/MM/DD/article-slug`. This structure allows for programmatic URL construction for date-based crawling. Archive pages might also be available, but direct URL manipulation is likely more efficient. The publication date on the article page can be used for filtering after extraction.

