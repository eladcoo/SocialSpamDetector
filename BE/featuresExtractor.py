
def extract_global_features(G):
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

def extract_local_features(G,communities):
    localFeatures = dict()
    for level in communities:
        for community_id in communities[level]:
            for node in communities[level][community_id]:
                num_of_sent = 0
                num_of_recieved = 0
                unique_out = 0
                unique_in = 0
                for edge in G.out_edges(node):
                    if edge[1] in communities[level][community_id]:
                        num_of_sent += G.get_edge_data(edge[0], edge[1])["weight"]
                        unique_out+=1
                for edge in G.in_edges(node):
                    if edge[0] in communities[level][community_id]:
                        num_of_recieved += G.get_edge_data(edge[0], edge[1])["weight"]
                        unique_in+=1

                details = {'local_distinct_senders':unique_out, 'local_distinct_recipients':unique_in, 'local_total_sent': num_of_sent,
                           'local_total_received': num_of_recieved}
                if(node not in localFeatures):
                    localFeatures[node] = {}
                localFeatures[node].update({f"{level}-{community_id}":details})


    print("localFeatures:",localFeatures)
    return localFeatures
