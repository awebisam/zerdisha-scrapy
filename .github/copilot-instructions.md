
# 🧠 GitHub Copilot Instructions for the `zerdisha-scrapy` Project

This document provides essential context and **strict guidelines** for GitHub Copilot when generating code for the `zerdisha-scrapy` repository.  
**Adherence to these rules is mandatory** to maintain code quality, consistency, and architectural integrity.

---

## 1. 📦 Core Project Identity & Architecture

- This project is a **data ingestion engine** built with **Python** and the **Scrapy** framework.
- Its sole purpose is to **crawl news websites**, extract article data, and prepare it for a separate downstream application.

### ❌ Do NOT:
- Generate code for **data analysis**, **API endpoints**, **user interfaces**, or **database storage**.
- Suggest deployment configurations for **Kubernetes**, **Docker**, or **generic servers**.

### ✅ Do:
- Design spiders suitable for deployment on **Zyte Scrapy Cloud** only.
- Use the package name: `zerdisha_scrapers`.

---

## 2. 🧾 The Data Contract: `ArticleItem`

All spiders **must yield** instances of `zerdisha_scrapers.items.ArticleItem`.  
This is the **single source of truth** for structured data.

### 🔐 Required Fields (must be non-empty strings):
- `url` (str): Canonical URL of the article.
- `source_name` (str): News publication name.
- `title` (str): Article headline.
- `full_text` (str): Complete article body.
- `scraped_at` (str): ISO 8601 timestamp when scraped.
- `spider_name` (str): Name of the spider.

### 🕊️ Optional Fields (set to `None` if unavailable):
- `author` (Optional[str]): Name of the author.
- `publication_date` (Optional[str]): Article's original publication date.

> **CRITICAL**:  
> All timestamp fields must be **timezone-aware** and formatted as **ISO 8601**.  
> Use:  
```python
datetime.now(timezone.utc).isoformat()
```

---

## 3. 🕷️ Spider Development Standards

- Use `zerdisha_scrapers/spiders/kathmandupost.py` as the **template and gold standard**.
- This spider demonstrates **hybrid RSS/Scrapy approach** with robust publication date extraction.

### ✅ Logging:
Use `self.logger` with proper levels:
- `self.logger.info()` – Lifecycle events (e.g. spider start).
- `self.logger.debug()` – Fine-grained progress tracking.
- `self.logger.warning()` – Recoverable issues (e.g. missing field).
- `self.logger.error()` – Exception handling.

### 🔁 Robust Parsing:
- Use `try...except` in the `parse()` method to catch and log errors.
- Prevent crashing on individual page failures.

### 📅 Publication Date Extraction:
- Implement multiple fallback strategies for date extraction
- Primary: Extract from article page elements (CSS selectors, meta tags)
- Fallback: Parse from URL structure (e.g., `/2025/07/03/`)
- Always validate and format dates to ISO 8601 format
- Handle cases where publication dates are unavailable gracefully

### ❌ Do NOT:
- Clean data (e.g. whitespace stripping)
- Format timestamps inside spiders

➡️ This logic is handled by:
- `ValidationPipeline`
- `CleaningPipeline`
- `TimestampPipeline`

---

## 4. 📐 Coding Standards: The Non-Negotiables

### 🚨 Strict Typing – REQUIRED
All code **must** include **type hints** for:
- Function/method arguments
- Return values
- Class attributes

**Example**:
```python
def parse(self, response: Response) -> Generator[ArticleItem, None, None]:
````

### 📄 Google-Style Docstrings – REQUIRED

Every **module**, **class**, and **function/method** must include a proper docstring.

**Example**:

```python
"""Extracts the article title from the response.

Args:
    response: The HTTP response object containing the page.

Returns:
    The extracted title as a string, or None if not found.
"""
```

---

## 5. 🧪 Testing Standards

* All new features and bug fixes **must** be accompanied by **unit tests**.
* Use **Python’s built-in `unittest` framework** only.
  ❌ Do not use `pytest` or other frameworks.

### 🔧 Mocking:

Use `unittest.mock`, especially `MagicMock`, to isolate units under test.

### 🔤 Naming Conventions:

* Test class names: `TestMyNewFeature`
* Test methods: Start with `test_` and describe the behavior
  e.g., `test_handles_invalid_input_gracefully`
