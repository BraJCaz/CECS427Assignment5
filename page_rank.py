# Brandon Cazares
# CECS 427 Sec 1
# Professor Ponce
# Due Date: 4/29/2025
# Assignment 5: Information Network and the WWW
import argparse
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
from crawler.run_crawler import run_scrapy_crawler

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------
# Argument Parsing
# ------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="PageRank with optional web crawler")
    parser.add_argument('--crawler', help='File containing crawler configuration')
    parser.add_argument('--input', help='Input graph in GML format')
    parser.add_argument('--loglogplot', action='store_true', help='Generate log-log degree plot of distribution')
    parser.add_argument('--crawler_graph', type=str, help='Path to save crawled graph (.gml)')
    parser.add_argument('--pagerank_values', type=str, help='Output path for PageRank values (.txt)')
    return parser.parse_args()

# ------------------------------------------------------------
# File Operations
# ------------------------------------------------------------
def read_graph(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Graph file not found: {file_path}")
    return nx.read_gml(file_path, label='id')

def write_pagerank_to_file(pagerank_dict, output_path):
    with open(output_path, 'w') as f:
        for node, score in sorted(pagerank_dict.items(), key=lambda x: -x[1]):
            f.write(f"{node} {score:.6f}\n")

# ------------------------------------------------------------
# Graph Visualization
# ------------------------------------------------------------
def draw_graph(graph, output_file="crawler_graph.png"):
    pos = nx.spring_layout(graph, k=0.5, iterations=50)
    plt.figure(figsize=(12, 10))
    nx.draw(graph, pos, with_labels=True, node_size=300, font_size=8,
            edge_color='gray', node_color='skyblue')
    plt.title("Crawled Graph")
    plt.savefig(output_file)
    print(f"[INFO] Saved graph visualization to {output_file}")
    plt.close()

def plot_loglog_degree_distribution(Graph, output_file="LogLog_1000-Nodes.png"):
    degree = [deg for _, deg in Graph.degree()]
    degree_counts = {}

    for d in degree:
        degree_counts[d] = degree_counts.get(d, 0) + 1

    # our x list
    x = list(degree_counts.keys())
    # our y list
    y = list(degree_counts.values())

    plt.figure()
    # our loglog plot will have blue dots
    plt.loglog(x, y, 'bo')
    plt.xlabel("Degree (log)")
    plt.ylabel("Number of Nodes (log)")
    plt.title("Log-Log Degree Distribution")
    plt.savefig(output_file)
    print(f"[INFO] Saved log-log plot to {output_file}")
    plt.show()
    plt.close()

# ------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------
def main():
    args = parse_args()
    Graph = None

    # Crawl or load input
    if args.crawler:
        print(f"[INFO] Crawling from: {args.crawler}")
        Graph = run_scrapy_crawler(args.crawler)
        if Graph:
            print(f"[INFO] Crawled {Graph.number_of_nodes()} nodes and {Graph.number_of_edges()} edges")
            if args.crawler_graph:
                nx.write_gml(Graph, args.crawler_graph)
                print(f"[INFO] Saved GML graph to {args.crawler_graph}")
            draw_graph(Graph)
        else:
            print("[WARNING] Crawler finished but returned no graph.")

    if Graph is None and args.input:
        try:
            Graph = read_graph(args.input)
            # this prints out info from a loaded graph file with the number of nodes
            print(f"[INFO] Loaded graph from file with {Graph.number_of_nodes()} nodes and {Graph.number_of_edges()} edges")
        except Exception as e:
            # this lets us know if there was a failure to load an input graph
            print(f"[ERROR] Failed to load input graph: {e}")
            exit(1)

    if Graph is None:
        # this error means no graph was created or loaded
        print("[ERROR] No graph was created or loaded.")
        # this checks out crawler.txt file
        print("If using --crawler, check your crawler.txt file and domain.")
        # this checks if the gml file is valid
        print("If using --input, check that the .gml file exists and is valid.")
        exit(1)

    # Compute PageRank
    print("[INFO] Computing PageRank...")
    pagerank = nx.pagerank(Graph)
    # this completes our PageRank computation
    print("[INFO] PageRank computation complete.")

    # Save PageRank values
    if args.pagerank_values:
        write_pagerank_to_file(pagerank, args.pagerank_values)
        print(f"[INFO] Saved PageRank values to {args.pagerank_values}")

    # Plot log-log distribution
    if args.loglogplot:
        plot_loglog_degree_distribution(Graph)

if __name__ == "__main__":
    main()
