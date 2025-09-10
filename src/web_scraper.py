"""
Target Website: books.toscrape.com (a practice website for web scraping)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import List, Dict
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BookScraper:
    """A web scraper for extracting book information from books.toscrape.com"""
    
    def __init__(self, base_url: str = "https://books.toscrape.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page_content(self, url: str) -> BeautifulSoup:
        """Fetch and parse webpage content"""
        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raise exception for bad status codes
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_book_data(self, book_url: str) -> Dict:
        """Extract detailed information from a book page"""
        soup = self.get_page_content(book_url)
        if not soup:
            return None
            
        book_info = {}
        
        try:
            # Extract book title
            book_info['title'] = soup.find('h1').text
            
            # Extract price
            price = soup.find('p', class_='price_color').text
            book_info['price'] = float(price.replace('£', ''))
            
            # Extract availability
            availability = soup.find('p', class_='instock availability').text
            book_info['availability'] = availability.strip()
            
            # Extract rating
            rating_classes = soup.find('p', class_='star-rating')['class']
            book_info['rating'] = rating_classes[1] if len(rating_classes) > 1 else 'No rating'
            
            # Extract product description
            description = soup.find('meta', attrs={'name': 'description'})['content']
            book_info['description'] = description.strip()
            
            # Extract product information from table
            table = soup.find('table', class_='table table-striped')
            for row in table.find_all('tr'):
                header = row.find('th').text
                value = row.find('td').text
                book_info[header.lower().replace(' ', '_')] = value.strip()
                
            book_info['url'] = book_url
            logger.info(f"Successfully scraped: {book_info['title']}")
            
        except Exception as e:
            logger.error(f"Error parsing book data from {book_url}: {e}")
            return None
            
        return book_info
    
    def get_all_books_from_page(self, page_url: str) -> List[Dict]:
        """Get all books from a catalog page"""
        soup = self.get_page_content(page_url)
        if not soup:
            return []
            
        books = []
        book_elements = soup.find_all('article', class_='product_pod')
        
        for book in book_elements:
            relative_url = book.find('h3').find('a')['href']
            # Handle relative URLs
            if relative_url.startswith('catalogue/'):
                full_url = f"{self.base_url}/catalogue/{relative_url.replace('../../', '')}"
            else:
                full_url = f"{self.base_url}/catalogue/{relative_url}"
                
            book_data = self.extract_book_data(full_url)
            if book_data:
                books.append(book_data)
            # Be respectful - add a small delay between requests
            time.sleep(0.5)
            
        return books
    
    def scrape_all_books(self, max_pages: int = None) -> List[Dict]:
        """Scrape books from all pages with pagination handling"""
        all_books = []
        page_num = 1
        next_page_url = f"{self.base_url}/catalogue/page-{page_num}.html"
        
        while next_page_url:
            if max_pages and page_num > max_pages:
                break
                
            logger.info(f"Scraping page {page_num}: {next_page_url}")
            soup = self.get_page_content(next_page_url)
            
            if not soup:
                break
                
            # Extract books from current page
            page_books = self.get_all_books_from_page(next_page_url)
            all_books.extend(page_books)
            
            # Check for next page
            next_button = soup.find('li', class_='next')
            if next_button:
                page_num += 1
                next_page_url = f"{self.base_url}/catalogue/page-{page_num}.html"
            else:
                next_page_url = None
                
            # Be respectful - add a delay between pages
            time.sleep(1)
            
        return all_books
    
    def save_to_csv(self, data: List[Dict], filename: str = 'scraped_books.csv'):
        """Save scraped data to CSV file"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename} with {len(data)} records")
        
    def save_to_json(self, data: List[Dict], filename: str = 'scraped_books.json'):
        """Save scraped data to JSON file"""
        df = pd.DataFrame(data)
        df.to_json(filename, orient='records', indent=4)
        logger.info(f"Data saved to {filename} with {len(data)} records")

def main():
    """Main function to run the web scraper"""
    scraper = BookScraper()
    
    # Scrape data (limit to 2 pages for demonstration)
    logger.info("Starting web scraping process...")
    books_data = scraper.scrape_all_books(max_pages=50)
    
    if books_data:
        # Save data in multiple formats
        scraper.save_to_csv(books_data, 'data/raw/scraped_books.csv')
        scraper.save_to_json(books_data, 'data/raw/scraped_books.json')
        logger.info(f"Scraping completed. Total books: {len(books_data)}")
    else:
        logger.error("No data was scraped.")

if __name__ == "__main__":
    main()