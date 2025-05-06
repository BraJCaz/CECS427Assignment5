# CECS427Assignment5 redo
# Brandon Cazares 
# Professor Ponce 
# Due Date: 5/13/2025
# Objective 
- This assignment requires us to solidy my understanding of web crawling by creating a graph on the internet using Python and applying the PageRank algorithm to identify the most relevant pages. Acquiring this knowledge will not only boost my programming skills but, it'll also enchace my comprehensiveness in an evolving Computer Science field.
# Requirement 
- This is the command to run our Python script in this assignment, rank_page.py located in the current directory and either reads the file graph or creates a graph by crawling on the internet starting with the given web address in crawler.txt. Here, graph.gml or the created graph is the graph that will be used as input for the PageRank algorithm and to plot the log plot.
- This assignment requires us to write a Python code that runs in a terminal because we need to understand that the program accepts optional parameters. The command to execute the Python program is this:
python ./page_rank.py --crawler crawler.txt --input graph.gml --loglogplot --crawler_graph out_graph.gml -- pagerank_values node_rank.txt
- When I ran this command, it gave me crawled 66 nodes and 65 edges, saved my GML to an output graph file, pagerank computed, saved page_rank values to node.txt, also save pagerank colored-graph to node.graph_png and node_link graph saved to node_graph.png
# Description of Parameters
- The script graph.py must be located in the current directory because that's how ensure robust files handle mechanisms such as error checking, file existence validation and appropriate error messages.
--crawler crawler.txt
- This specifies the file containing the initial web pages to crawl. The crawling must create a directed graph using scrapy and visiting only Html pages. The first value is an integer representing the maximum number of nodes to load the second line gives the domain to crawl; next are the web pages to start crawling.
- The format of the input file is:
n: Integer with the number of vertices (pages)
domain: String 
webpage_1: String 
webpage_2: String 
...
webpage_n: String  
For example
100
https://dblp.org/pid
https://dblp.org/pid/e/PErdos.html
https://dblp.org/pid/s/PaulGSpirakis.html
https://dblp.org/pid/89/8192.html
- I updated my crawler.txt file with 20 nodes instead of 100
20
https://dblp.org
https://dblp.org/pid/49/4862.html
https://dblp.org/pid/l/LeslieLamport.html
- We use this file to test Crawling 1:
-- input graph.gml
- This specifies the log-log plot of the degree distribution of the graph
--crawler_graph out_graph.gml 
- This saves the processed graph to out_graph.gml
--pagerank_values node_rank.txt
Examples:

python ./page_rank.py --crawler crawler.txt --loglogplot --crawler_graph out_graph.gml  --pagerank_values node_rank.txt
- This command prints out a directed graph using the crawling and the parameters in crawler.txt file because it also performs the Page rank algorithm in the created graph. It also plots the log plot, writes the resulting digraph in out_graph.gml and writes the page rank algorithm of all nodes in node_rank.txt.
- For example, when I ran this command on my machine, it gave me 20 max nodes, crawled 66 nodes and 65 edges, and the same exact results as command 1. 

python ./page_rank.py --input graph.gml --loglogplot --pagerank_values node_rank.txt
- Finally, this command above performs the Page rank algorithm in graph.gml plots the Log plot and writes the page of all nodes in node_rank.txt.
- For example, when I ran this command on my machine, it gave me a loaded graph from file with 4 nodes and 4 edges, it computed the pagerank algorithm, saved the pagerank values to node_rank.txt and it saved my log-log plot to 1000 nodes. 
