## The Himalayan Times

### Article Title
- CSS: `h1.article-title`
- XPath: `//h1[@class=\'article-title\']`
- Notes: The article title is within an `h1` tag with the class `article-title`.

### Full Article Text
- CSS: `.content-inner p`
- XPath: `//div[@class=\'content-inner\']//p`
- Notes: The main article content is within `<p>` tags inside a `div` with the class `content-inner`.

### Author Name
- CSS: `.author-name` or `span.byline`
- XPath: `//span[@class=\'author-name\']` or `//span[@class=\'byline\']`
- Notes: Author names are often within `span` tags with classes like `author-name` or `byline`.

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
- The Himalayan Times uses a URL structure that includes the article slug. The date is not directly in the URL, so date filtering will need to happen after extracting the publication date from the article page. There might be archive pages or sitemaps that could be explored for date-based navigation, but this would require further investigation.

