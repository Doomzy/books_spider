import re
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from books_spider.items import Book

class IndeedjobsSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        categoriesUrl=response.css('ul.nav-list ul li a::attr(href)').extract()

        for cat in categoriesUrl:
            catUrl= self.start_urls[0]+cat
            yield Request(catUrl,callback=self.catData)

    def catData(self,response):
        booksU=response.css('.product_pod h3 a::attr(href)').extract()
        for bu in booksU:
            bookUrl= self.start_urls[0]+'catalogue/'+bu[9:]
            yield Request(bookUrl,callback=self.bookData)
        nextPage=response.css('.next a::attr(href)').get()
        if nextPage is not None:
            nextPageUrl=re.sub(r'([^\/]+$)',str(nextPage),str(response.request.url))
            yield Request(nextPageUrl,callback=self.catData)

    def bookData(self,response):
        book=ItemLoader(item=Book())

        title=response.css('h1::text').extract()
        description=response.css('#product_description+ p::text').extract()
        price=response.css('tr:nth-child(4) td::text').extract()
        ucp=response.css('tr:nth-child(1) td::text').extract()

        book._add_value('title',title)
        book._add_value('description',description)
        book._add_value('price',price)
        book._add_value('ucp',ucp)
        yield book.load_item()