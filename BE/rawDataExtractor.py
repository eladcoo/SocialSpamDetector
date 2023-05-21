import os
import re
from collections import defaultdict
import chardet
from graphBuilder import createConnections


# Get the list of all files and directories
def extractFromDir(path):

    # Create base graph and graph to be sketched
    base_graph = defaultdict(list)
    num_of_invalid_files = 0
    # Add nodes and edges to base graph
    for path, subdirs, files in os.walk(path):
        for name in files:
            try:
                file_name = os.path.join(path, name)
                with open(file_name, 'rb') as file:
                    data = file.read()
                    encoding = chardet.detect(data)['encoding']

                with open(file_name, 'r', encoding=encoding) as search:
                    fromAddresses = []
                    toAddresses = []
                    for line in search:
                        line = line.rstrip()  # remove '\n' at end of line
                        if "@" not in line:
                            continue
                        if "From:" in line and line.index("From:") == 0:
                            fromAddresses = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", line)
                        if "To:" in line and line.index("To:") == 0:
                            toAddresses = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", line)
                    createConnections(base_graph,fromAddresses,toAddresses)
            except:
                print("invalid file:", name)
                num_of_invalid_files+=1
    print("num_of_invalid_files: ",num_of_invalid_files)
    return base_graph


def enrichGraphWithContent(G ,base_graph, tag = None):
    # calculate weights
    for srcNode in base_graph:
        #TODO what happens if G has nodes already?
        visitedNodes = []
        for dstNode in base_graph[srcNode]:
            if dstNode not in visitedNodes:
                count = base_graph[srcNode].count(dstNode)
                if (tag == None):
                    G.add_node(srcNode)
                else:
                    G.add_node(srcNode, color='red')
                visitedNodes.append(dstNode)
                print(srcNode + "," + dstNode + "," + str(count))
                G.add_edge(srcNode, dstNode, weight=count)

