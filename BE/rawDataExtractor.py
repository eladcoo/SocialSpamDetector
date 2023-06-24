import os
import re
from collections import defaultdict
import chardet

from BE.graphBuilder import createConnections

list_of_spam_words = {}
def load_spam_words():
    with open('../resources/spam-words.txt','r') as file:
        for line in file:
            line = line.strip()
            list_of_spam_words[line] = True


# Get the list of all files and directories
def extract_from_dir(path):

    # Create base graph and graph to be sketched
    base_graph = defaultdict(list)
    num_of_invalid_files = 0
    if not list_of_spam_words:
        load_spam_words()

    # Add nodes and edges to base graph
    for path, subdirs, files in os.walk(path):
        for name in files:
            try:
                file_name = os.path.join(path, name)
                with open(file_name, 'rb') as file:
                    data = file.read()
                    encoding = chardet.detect(data)['encoding']

                with open(file_name, 'r', encoding=encoding) as file:
                    from_addresses = []
                    to_addresses = []
                    is_spam = False
                    for line in file:
                        line = line.rstrip()  # remove '\n' at end of line
                        # check if line contains any spam words
                        for word in line.split():
                            if word in list_of_spam_words:
                                is_spam = True

                        if "@" not in line:
                            continue
                        if "From:" in line and line.index("From:") == 0:
                            from_addresses = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", line)
                        if "To:" in line and line.index("To:") == 0:
                            to_addresses = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", line)

                    createConnections(base_graph, from_addresses, to_addresses, is_spam)
            except:
                print("invalid file:", name)
                num_of_invalid_files += 1
    print("num_of_invalid_files: ", num_of_invalid_files)
    return base_graph


def is_a_spammer_node(dest_nodes):
    is_spam = False
    for dest_node in dest_nodes:
        is_spam = is_spam or dest_node['is_spam']
    return is_spam

#Build graph with tags and weights
def enrich_graph_with_content(G ,base_graph):
    spam_node_color = {True: 'red', False: 'blue'}
    for src_node in base_graph:
        visited_nodes = []
        is_spam = is_a_spammer_node(base_graph[src_node])
        if src_node in G.nodes():
            if is_spam:
                G.nodes[src_node]['color'] = 'red'
        else:
            G.add_node(src_node, color=spam_node_color[is_spam])

        for dest_node in base_graph[src_node]:
            if dest_node not in visited_nodes:
                count = base_graph[src_node].count(dest_node)
                visited_nodes.append(dest_node)
                print(src_node,",",dest_node,",",str(count))
                if dest_node['node'] not in G.nodes():
                    G.add_node(dest_node['node'], color='blue')
                G.add_edge(src_node, dest_node['node'], weight=count)

