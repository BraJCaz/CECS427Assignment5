# Brandon Cazares
# CECS 427 Sec 1
# Professor Ponce
# Due Date: 5/8/2025
# Assignment 5: Information Network and the WWW
# This is my updated code so please grade this one
import argparse
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
from crawler.run_crawler import run_scrapy_crawler

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Our Argument Parsing
def parse_args():
    parser = argparse.ArgumentParser(description="PageRank with optional web crawler")
    parser.add_argument('--crawler', help='File containing crawler configuration')
    parser.add_argument('--input', help='Input graph in GML format')
    parser.add_argument('--loglogplot', action='store_true', help='Generate log-log degree plot of distribution')
    parser.add_argument('--crawler_graph', type=str, help='Path to save crawled graph (.gml)')
    parser.add_argument('--pagerank_values', type=str, help='Output path for PageRank values (.txt)')
    return parser.parse_args()
# Our File Operations
def read_graph(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Graph file not found: {file_path}")
    return nx.read_gml(file_path, label='id')

def write_pagerank_to_file(pagerank_dict, output_path):
    with open(output_path, 'w') as f:
        for node, score in sorted(pagerank_dict.items(), key=lambda x: -x[1]):
            f.write(f"{node} {score:.6f}\n")
# Graph Visualization
# First, we draw our graph to get our node-link graph
def draw_graph(graph, pagerank_scores=None, output_file="node_graph.png"):
    pos = nx.spring_layout(graph, k=0.5, iterations=50)  # Spring layout

    # Scale node sizes by PageRank (if provided)
    if pagerank_scores:
        node_sizes = [pagerank_scores[node] * 5000 for node in graph.nodes()]
    else:
        node_sizes = [500 for _ in graph.nodes()]  # Default size if PageRank missing

    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(graph, pos,
                           node_color='skyblue',       # Fixed color
                           node_size=node_sizes)       # Scaled size
    # Always draw edges
    nx.draw_networkx_edges(graph, pos, edge_color='gray', arrows=True)

    # Only draw labels for small graphs
    if len(graph.nodes()) <= 100:
        nx.draw_networkx_labels(graph, pos, font_size=4)
        nx.draw_networkx_edges(graph, pos, edge_color='gray', arrows=True)

    plt.title("Node-Link Graph (Spring Layout, Blue Nodes, Size by PageRank)")
    plt.savefig(output_file)
    print(f"[INFO] Saved PageRank-colored graph to {output_file}")
    plt.show()
    plt.close()
# we will do both a load graph and compute page rank
def load_graph_and_compute_pagerank(gml_path):
    Graph = nx.read_gml(gml_path)
    if not nx.is_directed(Graph):
        Graph = Graph.to_directed()
    pagerank_scores = nx.pagerank(Graph)
    return Graph, pagerank_scores
# then, we plot our log graph
def plot_loglog_degree_distribution(Graph):
    degrees = [Graph.degree(n) for n in Graph.nodes()]
    degree_count = {}
    for d in degrees:
        degree_count[d] = degree_count.get(d, 0) + 1

    # our x list
    x = list(degree_count.keys())
    # our y list
    y = list(degree_count.values())

    plt.figure()
    plt.loglog(x, y, marker='o', linestyle='None')
    # x label
    plt.xlabel("Degree (log)")
    # y label
    plt.ylabel("Frequency (log)")
    # log plot title
    plt.title("Log-Log Degree Distribution")
    plt.grid(True)
    # our log file when saved
    plt.savefig("loglog_plot.png")
    plt.show()
    plt.close()
# Now, we have our save pagerank scores
def save_pagerank_scores(pagerank_scores, output_file):
    with open(output_file, 'w') as f:
        for node, score in sorted(pagerank_scores.items(), key=lambda x: -x[1]):
            f.write(f"{node} {score:.6f}\n")
# Our Main Execution driver
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
                # this saves the saved graph GML graph file
                print(f"[INFO] Saved GML graph to {args.crawler_graph}")
        else:
            # this gives us a warning when a crawler didn't finish with a graph
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
        draw_graph(Graph, pagerank_scores=pagerank, output_file="node_graph.png")  # node plot FIRST
        print("[INFO] Node-link graph saved as node_graph.png")
        plot_loglog_degree_distribution(Graph)

if __name__ == "__main__":
    main()