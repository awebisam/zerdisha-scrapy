## The Annapurna Express

### Article Title
- CSS: `h1.single-title`
- XPath: `//h1[@class=\'single-title\']`
- Notes: The article title is within an `h1` tag with the class `single-title`.

### Full Article Text
- CSS: `.single-content p`
- XPath: `//div[@class=\'single-content\']//p`
- Notes: The main article content is within `<p>` tags inside a `div` with the class `single-content`.

### Author Name
- CSS: `.author-name` or `span.byline`
- XPath: `//span[@class=\'author-name\']` or `//span[@class=\'byline\']`
- Notes: Author names are often within `span` tags with classes like `author-name` or `byline`. Sometimes it's prefixed with 'By:'.

### Publication Date
- CSS: `.published-date` or `time`
- XPath: `//span[@class=\'published-date\']` or `//time`
- Notes: Dates are usually within `span` tags with class `published-date` or `time` tags. The format is typically human-readable and needs parsing.

### Article URL
- Canonical URL: Look for `<link rel="canonical" href="...">` in the HTML head.
- Notes: The article URL is the current page URL. Canonical URLs are usually present in the `<head>` section.

### Tags or Categories
- CSS: `.tags a` or `.category a`
- XPath: `//div[@class=\'tags\']//a` or `//div[@class=\'category\']//a`
- Notes: Tags and categories are often links within `div` elements with classes like `tags` or `category`.

### Navigation and Date Filtering
- The Annapurna Express uses a URL structure like `https://theannapurnaexpress.com/story/article-id/`. The date is not directly in the URL, so date filtering will need to happen after extracting the publication date from the article page. There might be archive pages or sitemaps that could be explored for date-based navigation, but this would require further investigation.

