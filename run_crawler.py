# Brandon Cazares
# CECS 427 Sec 1
# Professor Ponce
# Due Date: 4/29/2025
# Assignment 5: Information Network and the WWW
import scrapy
import networkx as nx  # Make sure this is imported
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings  # <-- add this import
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer

class LinkCollector:
    def __init__(self):
        self.edges = []  # Store edges as (source, target)

    def collect(self, item):
        self.edges.append((item['source'], item['target']))

    def to_networkx_graph(self):
        Graph = nx.DiGraph()
        Graph.add_edges_from(self.edges)
        return Graph
class MySpider(scrapy.Spider):
    name = "dblp_spider"

    def __init__(self, collector=None, config_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collector = collector
        self.max_nodes, self.domain, self.start_urls = parse_crawler_config(config_path)
        self.visited_urls = set()

    def start_requests(self):
        for url in self.start_urls:
            if self.domain in url:
                self.visited_urls.add(url)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if len(self.visited_urls) >= self.max_nodes:
            return

        current_url = response.url

        for link in response.css('a::attr(href)').getall():
            absolute_link = response.urljoin(link)

            # Stay inside domain
            if self.domain not in absolute_link:
                continue

            # Avoid visiting the same URL twice
            if absolute_link in self.visited_urls:
                continue

            # Collect the edge
            self.collector.collect({'source': current_url, 'target': absolute_link})

            self.visited_urls.add(absolute_link)

            # Only follow if we still need more nodes
            if len(self.visited_urls) < self.max_nodes:
                yield scrapy.Request(url=absolute_link, callback=self.parse)
# Next, we run our parse crawler configuration
def parse_crawler_config(config_file):
    with open(config_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    max_nodes = int(lines[0])
    domain = lines[1]
    start_urls = lines[2:]
    print(f"[DEBUG] max_nodes = {max_nodes}")
    print(f"[DEBUG] domain = {domain}")
    print(f"[DEBUG] start_urls = {start_urls}")

    return max_nodes, domain, start_urls

# then, we run our scarpy crawler
def run_scrapy_crawler(config_file):
    max_nodes, domain, start_urls = parse_crawler_config(config_file)

    # Fast crawler settings
    settings = Settings()
    settings.set('CONCURRENT_REQUESTS', 64)  # 4x faster
    settings.set('DOWNLOAD_DELAY', 0)         # no waiting
    settings.set('RETRY_ENABLED', False)      # no retries
    settings.set('REDIRECT_ENABLED', False)   # no redirects
    settings.set('LOG_LEVEL', 'WARNING')      # cleaner output

    process = CrawlerProcess(settings)

    collector = LinkCollector()

    process.crawl(MySpider, collector=collector, config_path=config_file)
    process.start()

    graph = collector.to_networkx_graph()
    return graph