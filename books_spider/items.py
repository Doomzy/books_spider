from itemloaders.processors import Join
import scrapy


class Book(scrapy.Item):
   title=scrapy.Field(output_processor=Join())
   description=scrapy.Field(output_processor=Join())
   price=scrapy.Field(output_processor=Join())
   ucp=scrapy.Field(output_processor=Join())