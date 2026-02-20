# WebMiniSearch

> A lightweight, self-contained web search engine built with Python and Flask.  
> Crawls a target website, indexes its content, and serves search results through a minimal web interface.

---

## Overview

WebMiniSearch is a full-pipeline search engine prototype consisting of three components:

- **Crawler** — recursively follows internal links on a target website and extracts page content
- **Indexer** — stores and ranks page content using [Whoosh](https://whoosh.readthedocs.io/), a pure-Python full-text search library
- **Search Interface** — a Flask web application that accepts queries and returns ranked results

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Crawling | `requests`, `BeautifulSoup4` |
| Indexing & Search | `Whoosh` (StemmingAnalyzer, QueryParser) |
| NLP | `NLTK` (tokenization, stopwords, Porter stemming) |
| Web Framework | `Flask` |
| Deployment | Apache + `mod_wsgi` |

---

## Project Structure

```
WebMiniSearch/
│
├── crawler.py              # Crawls the target website and builds the Whoosh index
├── query_parser.py         # Processes search queries and retrieves ranked results
├── search_engine.py        # Flask application — routes and rendering
├── utils.py                # Shared utilities: text cleaning, NLTK resource loader
├── search.wsgi             # WSGI entry point for Apache deployment
├── requirements.txt        # Python dependencies
│
├── indexdir/               # Pre-built Whoosh index (ready to use)
│
└── templates/
    ├── start.html              # Search home page
    └── search_for_pages.html   # Search results page
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/yourusername/WebMiniSearch.git
cd WebMiniSearch
pip install -r requirements.txt
```

### Running Locally

```bash
flask --app search_engine run
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

> **Note:** A pre-built index is already included in `indexdir/`. You do not need to run the crawler unless you want to re-index.

### Rebuilding the Index

```bash
python crawler.py
```

This will crawl the target website from scratch and overwrite the existing index.

---

## Configuration

| Environment Variable | Description | Default |
|---|---|---|
| `NLTK_DATA_DIR` | Path to a custom NLTK data directory | System default |

```bash
export NLTK_DATA_DIR=/path/to/nltk_data
flask --app search_engine run
```

---

## Ranking Strategy

Pages are ranked using Whoosh's built-in BM25F scoring with the following customization:

- **Title field** is weighted at `2x` relative to body content
- Query tokens are **stemmed** (Porter Stemmer) before lookup to match morphological variants
- **Stop words** are removed from queries before processing

---

## Deployment

For production deployment on Apache with `mod_wsgi`:

1. Update the paths in `search.wsgi` to match your server directory
2. Configure your Apache virtual host to point to `search.wsgi` as the WSGI entry point

```apache
WSGIScriptAlias / /path/to/WebMiniSearch/search.wsgi
```

---

## Known Limitations

- The OpenAI-based page summarization feature in `crawler.py` is currently disabled (requires a valid API key). Page full-text is shown in place of summaries.
- The crawler is scoped to a single domain — it will not follow external links.

---

