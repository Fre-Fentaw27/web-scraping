# web-scraping

Data Collection and Web Scraping

## 📌 Overview

This project demonstrates web scraping techniques to collect book data from books.toscrape.com. The implementation handles pagination, extracts structured data, and saves it in CSV and JSON formats.

## 📂 Project Structure

```bash
web-scraping/
├── .venv/ # Virtual environment
├── data/
│ ├── raw/
│ └── scraped_books.csv # Raw complaint data
│ └── scraped_books.json # Raw complaint data
│ ├──preprocessed/
├── src/
│ └── web_scraper.py # Python script version of Task 2
├── .gitignore/ # to exclude files
└── requirements.txt
└── README.md
```

## Task 1: Data Collection and Web Scraping

### Features

- **Robust Web Scraping**: Extracts book information including title, price, rating, availability, and description
- **Pagination Handling**: Automatically navigates through multiple pages
- **Error Handling**: Comprehensive error handling and logging
- **Respectful Scraping**: Includes delays between requests to avoid overwhelming the target website
- **Multiple Output Formats**: Saves data in both CSV and JSON formats

### Setup

1.  **Clone the repository** (if applicable) or ensure you have the project structure locally.
2.  **Navigate to the project root directory** in your terminal.
3.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    ```
4.  **Activate the virtual environment**:
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
5.  **Install dependencies**:
    This project relies on `pandas`, `beautifulsoup4`, `requests` ,`matplotlib` ,`seaborn` ,`lxml`

### Usage

1. **Run the main scraping script**:
   ```bash
    python src/web_scraper.py
   ```

The script will:

- Scrape book data from books.toscrape.com (50 pages)

- Save raw data to data/raw/scraped_books.csv and data/raw/scraped_books.json

## Outputs

The scraper collects the following data for each book:

- Title

- Price

- Availability status

- Rating

- Description

- Product information (category, ISBN, etc.)

- URL
