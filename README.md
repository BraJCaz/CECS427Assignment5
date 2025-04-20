# CECS427Assignment5
# Brandon Cazares 
# Professor Ponce 
# Due Date: 4/29/2025
# Objective 
- This assignment requires us to solidy my understanding of web crawling by creating a graph on the internet using Python and applying the PageRank algorithm to identify the most relevant pages. Acquiring this knowledge will not only boost my programming skills but, it'll also enchace my comprehensiveness in an evolving Computer Science field.
# Requirement 
- This is the command to run our Python script in this assignment, rank_page.py located in the current directory and either reads the file graph or creates a graph by crawling on the internet starting with the given web address in crawler.txt. Here, graph.gml or the created graph is the graph that will be used as input for the PageRank algorithm and to plot the log plot.
- This assignment requires us to write a Python code that runs in a terminal because we need to understand that the program accepts optional parameters. The command to execute the Python program is this:
python ./page_rank.py --crawler crawler.txt --input graph.gml --loglogplot --crawler_graph out_graph.gml -- pagerank_values node_rank.txt
# Description of Parameters
- The script graph.py must be located in the current directory because that's how ensure robust files handle mechanisms such as error checking, file existence validation and appropriate error messages.
--crawler crawler.txt
- This specifies the file containing the initial web pages to crawl. The crawling must create a directed graph using scrapy and visiting only Html pages. The first value is an integer representing the maximum number of nodes to load the second line gives the domain to crawl; next are the web pages to start crawling.
- 
