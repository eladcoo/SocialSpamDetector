def addEdge(graph, u, v, is_spam):
    graph[u].append({'node': v, 'is_spam':is_spam})

def createConnections(graph,fromAddresses,toAddresses,is_spam):
    for fromAddress in fromAddresses:
        for toAddress in toAddresses:
            addEdge(graph, fromAddress, toAddress, is_spam)

