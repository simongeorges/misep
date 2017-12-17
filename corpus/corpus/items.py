import scrapy


class InlinksItem(scrapy.Item):
    # The source URL
    source = scrapy.Field()
    # The destination URL
    target = scrapy.Field()


class CorpusItem(scrapy.Item):
    # The source URL
    url = scrapy.Field()
    # TITLE tag
    title = scrapy.Field()
    # BODY tag
    body = scrapy.Field()

