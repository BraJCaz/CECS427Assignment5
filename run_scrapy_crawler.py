import networkx as nx
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.my_spider import MySpider  # Assuming your spider is under crawler/spiders/my_spider.py

# First, define your LinkCollector (this was missing!)
class LinkCollector:
    def __init__(self):
        self.edges = []  # list to store (source, target) edges

    def collect(self, item):
        self.edges.append((item['source'], item['target']))

    def to_networkx_graph(self):
        G = nx.DiGraph()  # Directed graph
        G.add_edges_from(self.edges)
        return G

# Assuming you already have parse_crawler_config
def parse_crawler_config(config_file):
    with open(config_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    max_nodes = int(lines[0])
    domain = lines[1]
    start_urls = lines[2:]
    return max_nodes, domain, start_urls

# Now the fixed run_scrapy_crawler
def run_scrapy_crawler(config_file):
    max_nodes, domain, start_urls = parse_crawler_config(config_file)

    settings = get_project_settings()

    process = CrawlerProcess(settings)

    collector = LinkCollector()

    process.crawl(MySpider, collector=collector, config_path=config_file)
    process.start()  # <--- Only start the reactor once!

    graph = collector.to_networkx_graph()
    return graph
