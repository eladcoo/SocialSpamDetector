def addEdge(graph, u, v):
    graph[u].append(v)

def createConnections(graph,fromAddresses,toAddresses):
    for fromAddress in fromAddresses:
        for toAddress in toAddresses:
            addEdge(graph, fromAddress, toAddress)

# definition of function
def generate_edges(graph):
    edges = []

    # for each node in graph
    for node in graph:

        # for each neighbour node of a single node
        for neighbour in graph[node]:
            # if edge exists then append
            edges.append((node, neighbour))
    return edges

