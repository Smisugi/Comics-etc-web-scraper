import scrapy

from comics.items import ComicsItem

class ComicSpider(scrapy.Spider):
    name = "comic"
    allowed_domains = ["www.comicsetc.com.au"]
    start_urls = ["https://www.comicsetc.com.au/collections/comics"]
    
    def start_requests(self):
        #runs error if no response
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.log_error)

    def parse(self, response):
        #test scraping
        """
        @url https://www.comicsetc.com.au/collections/comics
        @returns items 20 40
        @returns request 1 50
        @scrapes url title price
        """
        for comic in response.css("article.product.product-item.text-center"):
            item = ComicsItem()
            item["url"] = comic.css("a::attr(href)").get()
            item["title"] = comic.css("h4.product-item__title::text").get()
            item["price"] = comic.css("span.product-item__price::text").get()
            yield item
            
        next_page = response.css("span.next > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(
                f"Scraping next page: {next_page_url}"
            )
            yield scrapy.Request(url=next_page_url, callback=self.parse, errback=self.log_error)
    
    def log_error(self, failure):
        self.logger.error(repr(failure))
        #logs the error
        

