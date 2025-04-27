import scrapy

class MySpider(scrapy.Spider):
    name = "my_spider"

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', [])
        self.collector = kwargs.get('collector', None)

    def start_requests(self):
        print(f"[DEBUG] start_requests with {len(self.start_urls)} URLs")
        for url in self.start_urls:
            print(f"[DEBUG] Crawling: {url}")
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(f"[DEBUG] Visiting: {response.url}")
        for link in response.css("a::attr(href)").getall():
            absolute_link = response.urljoin(link)
            print(f"[DEBUG] Found link: {absolute_link}")
            item = {'source': response.url, 'target': absolute_link}
            if self.collector:
                self.collector.collect(item)
            yield scrapy.Request(absolute_link, callback=self.parse)