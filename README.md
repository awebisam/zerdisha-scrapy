# Zerdisha Scrapers [Entirely Built By Layers of AI Agents]

## Read the [Process](https://github.com/awebisam/zerdisha-scrapy/blob/main/PROCESS.md) for detailed breakdown. 

A robust, scalable data ingestion engine for gathering news articles from sources worldwide, built with Scrapy and designed for deployment on Zyte Scrapy Cloud.

## Project Purpose

The `zerdisha-scrapy` project is the dedicated data collection component of the Zerdisha ecosystem. It serves as an independent, specialized system responsible for:

- **Web Crawling**: Systematically discovering and accessing news articles from various sources
- **Data Extraction**: Parsing and structuring article content into standardized formats  
- **Data Pipeline**: Processing and preparing scraped data for consumption by the main Zerdisha application

This project operates independently from the main [Zerdisha](https://github.com/awebisam/zerdisha) API and frontend, enabling specialized deployment strategies and focused development of data ingestion capabilities.

## Architectural Overview

### Separation of Concerns

The project follows a clean architectural pattern where data ingestion is completely decoupled from data analysis and presentation:

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   zerdisha-scrapy   │───▶│   Data Storage      │───▶│      Zerdisha       │
│   (Data Collection) │    │   (Structured Data) │    │   (Analysis & API)  │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### Key Benefits

- **Independent Deployment**: Deploy scrapers to specialized platforms like Zyte Scrapy Cloud
- **Scalability**: Scale data collection independently from application logic
- **Maintainability**: Focused codebase with clear responsibilities  
- **Flexibility**: Easy to add new sources without affecting the main application

### Data Contract

All scraped data follows the `ArticleItem` schema, ensuring consistency across all sources:

- **url**: Canonical article URL
- **source_name**: News source identifier
- **title**: Article headline
- **full_text**: Complete article content
- **author**: Article author (when available)
- **publication_date**: Original publication timestamp (ISO 8601)
- **scraped_at**: Collection timestamp (ISO 8601)
- **spider_name**: Collecting spider identifier

### Publication Date Extraction

The spiders implement robust publication date extraction with multiple fallback strategies:

1. **Primary extraction**: Parse publication dates from article page elements
2. **URL structure fallback**: Extract dates from URL patterns (e.g., `/2025/07/03/`)
3. **Validation**: All dates are validated and formatted to ISO 8601 standard
4. **Error handling**: Graceful handling when dates cannot be determined

This ensures reliable date information even when news sources don't provide easily parseable publication dates.

## Getting Started

### Prerequisites

- Python 3.8+
- pip package manager or Poetry

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/awebisam/zerdisha-scrapy.git
   cd zerdisha-scrapy
   ```

2. **Install dependencies**:
   
   **Using pip**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Using Poetry** (recommended):
   ```bash
   poetry install
   poetry shell
   ```

3. **Verify installation**:
   ```bash
   scrapy version
   ```

### Running Spiders

1. **List available spiders**:
   ```bash
   scrapy list
   ```

2. **Run the Kathmandu Post spider**:
   ```bash
   scrapy crawl kathmandupost
   ```

3. **Run with limited items for testing**:
   ```bash
   scrapy crawl kathmandupost -s CLOSESPIDER_ITEMCOUNT=5
   ```

4. **Run with output to file**:
   ```bash
   scrapy crawl kathmandupost -o articles.json
   ```

### Project Structure

```
zerdisha-scrapy/
├── scrapy.cfg                 # Scrapy project configuration
├── zerdisha_scrapers/         # Main project package
│   ├── __init__.py
│   ├── items.py              # Data structure definitions (ArticleItem)
│   ├── middlewares.py        # Custom middleware components
│   ├── pipelines.py          # Data processing pipelines
│   ├── settings.py           # Project settings and configuration
│   └── spiders/              # Spider implementations
│       ├── __init__.py
│       └── kathmandupost.py  # Kathmandu Post hybrid RSS/Scrapy spider
└── README.md                 # This file
```

## How to Contribute

We follow strict coding standards to ensure high-quality, maintainable code:

### Coding Standards

1. **Strict Typing**: All Python code must include type hints - this is non-negotiable
   ```python
   def parse_article(self, response: Response) -> Generator[ArticleItem, None, None]:
   ```

2. **Comprehensive Documentation**: Every module, class, and function must include clear docstrings using Google Style
   ```python
   def extract_title(self, response: Response) -> Optional[str]:
       """Extract article title from the response.
       
       Args:
           response: The HTTP response object containing the page.
           
       Returns:
           The extracted title string, or None if not found.
       """
   ```

3. **Modern Python Practices**: Use current Python idioms and Scrapy best practices
4. **Readability First**: Write code for humans first, machines second

### Development Workflow

1. **Fork and clone** the repository
2. **Create a feature branch** for your changes
3. **Follow the coding standards** outlined above
4. **Test your changes** thoroughly
5. **Submit a pull request** with clear description

### Adding New Spiders

When creating new spiders, use the `kathmandupost.py` spider as your template. This spider demonstrates best practices including:

- **Hybrid RSS/Scrapy approach**: Efficient article discovery via RSS with comprehensive content extraction
- **Robust date extraction**: Multiple fallback strategies for publication date extraction
- **Error handling**: Comprehensive exception handling and logging
- **URL parsing**: Smart date extraction from URL structure when article pages don't provide clear dates

Ensure your spider:

- Inherits from `scrapy.Spider`
- Uses strict typing throughout
- Implements comprehensive logging with `self.logger`
- Properly populates `ArticleItem` instances
- Handles errors gracefully with try/except blocks
- Includes thorough documentation
- Extracts publication dates reliably (with fallback strategies)

### Example Spider Creation

```bash
# Generate a new spider using Scrapy's generator
scrapy genspider news_source example-news.com

# Then customize it following our standards and the kathmandupost.py template
```

## Deployment

This project is designed for deployment on **Zyte Scrapy Cloud**, which provides:

- Managed Scrapy hosting
- Automatic scaling
- Monitoring and logging
- Data export capabilities

Deployment configurations and instructions will be added as the project matures.

## License

This project is released into the public domain under The Unlicense. See [LICENSE](LICENSE) for details.
