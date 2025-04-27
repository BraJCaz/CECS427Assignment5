# Brandon Cazares
# CECS 427 Sec 1
# Professor Ponce
# Due Date: 4/22/2025
# Assignment 5: Information Network and the WWW
import scrapy

class EatsSpider(scrapy.Spider):
    name = 'eats_spider'

    def __init__(self, maximum_nodes, allowed_domain, start_urls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.allowed_domains = [allowed_domain.replace("https://", "").replace("http://", "")]
        self.visited = set()
        self.maximum_nodes = int(maximum_nodes)
        self.edges_file = open("edges.txt", "w")

# now, we parse our results
def parse(self, response):
    if len(self.visited) >= self.maximum_nodes:
        return
    self.visited.add(response.url)

    for href in response.css('a::attr(href)').getall():
        url = response.urljoin(href)
        if self.allowed_domains[0] in url and url not in self.visited:
            self.edges_file.write(f"{response.url} {url}\n")
            yield scrapy.Request(url, callback=self.parse)

# here, we close our results
def closed(self):
    self.edges_file.close()

