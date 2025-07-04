# Scrapy settings for zerdisha_scrapers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "zerdisha_scrapers"

SPIDER_MODULES = ["zerdisha_scrapers.spiders"]
NEWSPIDER_MODULE = "zerdisha_scrapers.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# This USER_AGENT identifies our scraper and links back to our GitHub repository
# for transparency and compliance with ethical scraping practices
USER_AGENT = "zerdisha_scrapers (+https://github.com/awebisam/zerdisha-scrapy)"

# Obey robots.txt rules
# Always respect robots.txt to maintain ethical scraping practices
# and avoid potential legal issues with content providers
ROBOTSTXT_OBEY = True

# Respect rate limits and server resources
# These settings ensure we don't overwhelm target servers
# Adjust these values based on target site capacity and requirements
CONCURRENT_REQUESTS_PER_DOMAIN = 1  # Conservative: one request at a time per domain
DOWNLOAD_DELAY = 1  # Wait 1 second between requests to same domain

# AutoThrottle settings for adaptive request timing
# Automatically adjusts delays based on server response times
# Uncomment and tune these for production deployments
#AUTOTHROTTLE_ENABLED = True
#AUTOTHROTTLE_START_DELAY = 5      # Initial delay
#AUTOTHROTTLE_MAX_DELAY = 60       # Maximum delay in high latency situations  
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Average concurrent requests per server
#AUTOTHROTTLE_DEBUG = False        # Enable to see throttling stats in logs

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "zerdisha_scrapers.middlewares.ZerdishaScrapersSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "zerdisha_scrapers.middlewares.ZerdishaScrapersDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zerdisha_scrapers.pipelines.ValidationPipeline': 300,
    'zerdisha_scrapers.pipelines.CleaningPipeline': 400,
    'zerdisha_scrapers.pipelines.TimestampPipeline': 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
