list_of_real_spammers = set()
list_of_real_hammers = set()

# The spam is tagged on the edge
def addEdge(graph, u, v, is_spam):
    graph[u].append({'node': v, 'is_spam':is_spam})

def createConnections(graph,fromAddresses,toAddresses,is_spam, is_real_spam):

    for fromAddress in fromAddresses:
        for toAddress in toAddresses:
            addEdge(graph, fromAddress, toAddress, is_spam)
            if is_real_spam:
                list_of_real_spammers.add(fromAddress)
                if fromAddress in list_of_real_hammers:
                    list_of_real_hammers.discard(fromAddress)
                if toAddress not in list_of_real_spammers:
                    list_of_real_hammers.add(toAddress)
            else:
                if fromAddress not in list_of_real_spammers:
                    list_of_real_hammers.add(fromAddress)
                if toAddress not in list_of_real_spammers:
                    list_of_real_hammers.add(toAddress)

def getAmounts():
    return list_of_real_spammers, list_of_real_hammers