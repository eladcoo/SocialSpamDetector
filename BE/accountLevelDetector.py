from spammerCommunitiesDetector import createDandogram

def extractGlobalFeatures(G):
    globalFeatures = dict()
    for node in G.nodes():
        num_of_sent = 0
        num_of_recieved = 0
        for edge in G.out_edges(node):
            num_of_sent+=G.get_edge_data(edge[0],edge[1])["weight"]
        for edge in G.in_edges(node):
            num_of_recieved+=G.get_edge_data(edge[0],edge[1])["weight"]
        details = {'global_distinct_senders':len(G.out_edges(node)),'global_distinct_recipients':len(G.in_edges(node)),
                   'global_total_sent':num_of_sent,'global_total_received':num_of_recieved}
        globalFeatures[node]=details

    return globalFeatures

def extractLocalFeatures(G):
    communities = createDandogram(G)
    print("communities:",communities)

    localFeatures = dict()
    for community_id in communities:
        for node in communities[community_id]:
            num_of_sent = 0
            num_of_recieved = 0
            unique_out = 0
            unique_in = 0
            for edge in G.out_edges(node):
                if edge[1] in communities[community_id]:
                    num_of_sent += G.get_edge_data(edge[0], edge[1])["weight"]
                    unique_out+=1
            for edge in G.in_edges(node):
                if edge[0] in communities[community_id]:
                    num_of_recieved += G.get_edge_data(edge[0], edge[1])["weight"]
                    unique_in+=1

            details = {'local_distinct_senders':unique_out, 'local_distinct_recipients':unique_in, 'local_total_sent': num_of_sent,
                       'local_total_received': num_of_recieved}
            localFeatures[node] = details


    print("localFeatures:",localFeatures)
    return localFeatures
