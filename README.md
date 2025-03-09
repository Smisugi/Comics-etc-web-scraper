
# Web Scraper for Comics Etc

A powerful and flexible web scraping tool built with Python, Scrapy, and MongoDB for efficient data extraction and storage.

## Features

- High-performance web crawling with Scrapy
- Automatic data extraction from websites
- Customizable scraping rules and patterns
- MongoDB integration for efficient data storage
- Rate limiting to respect website policies
- User-agent rotation to avoid detection
- Proxy support for anonymized scraping
- Export data in multiple formats (JSON, CSV, XML)
- Scheduling capabilities for periodic scraping

## Requirements

- Python 3.8+
- MongoDB 4.4+
- Scrapy 2.5+
- pymongo 4.0+

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Smisugi/Comics-etc-web-scraper.git
cd Comics-etc-web-scraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure MongoDB is running on your system.

## Configuration

1. Set up your MongoDB connection in `settings.py`:
```python
# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'scraper_data'
```

2. Configure your scraping settings in `settings.py`:
```python
# Crawl responsibly by identifying yourself on the user agent
USER_AGENT = 'YourWebScraper (+http://www.yourwebsite.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16
```

## Usage

### Creating a New Spider

1. Generate a new spider:
```bash
scrapy genspider example example.com
```

2. Edit the spider file in `spiders/example.py`:
```python
import scrapy
from scrapy.loader import ItemLoader
from web_scraper.items import WebScraperItem

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com']
    
    def parse(self, response):
        for product in response.css('div.product'):
            loader = ItemLoader(item=WebScraperItem(), selector=product)
            loader.add_css('name', 'h2.title::text')
            loader.add_css('price', 'span.price::text')
            loader.add_css('description', 'div.description::text')
            yield loader.load_item()
            
        # Follow pagination links
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

### Running a Spider

Run your spider with:
```bash
scrapy crawl example
```

To save the output to MongoDB:
```bash
scrapy crawl example -s ITEM_PIPELINES='{"web_scraper.pipelines.MongoDBPipeline": 300}'
```

### Exporting Data

Export data to various formats:
```bash
# JSON format
scrapy crawl example -o data.json

# CSV format
scrapy crawl example -o data.csv

# XML format
scrapy crawl example -o data.xml
```



### Adding a New Pipeline

Create a custom pipeline in `pipelines.py`:
```python
from itemadapter import ItemAdapter
import pymongo

class CustomProcessingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Process the item
        return item
```

### Creating a Middleware for Proxy Rotation

Add a proxy rotation middleware in `middlewares.py`:
```python
import random
from scrapy import signals

class ProxyMiddleware:
    def __init__(self, proxies):
        self.proxies = proxies
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('PROXY_LIST'))
    
    def process_request(self, request, spider):
        if self.proxies:
            request.meta['proxy'] = random.choice(self.proxies)
```

## Scheduling Scraping Jobs

Use a scheduler like cron (Linux/Mac) or Task Scheduler (Windows) to run your scraper periodically:

```bash
# Example crontab entry (Linux/Mac) to run daily at 2 AM
0 2 * * * cd /path/to/web-scraper && /path/to/venv/bin/python -m scrapy crawl example
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Make sure MongoDB is running
2. **Rate Limited/Blocked**: Reduce request frequency or use proxies
3. **Data Not Extracted**: Check your CSS/XPath selectors

## License

This project is licensed under the MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

Kirt - jkirtcado@gmail.com

Project Link: [https://github.com/Smisugi/Comics-etc-web-scraper]
