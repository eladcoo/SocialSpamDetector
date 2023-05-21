import community as community_louvain

from communityManager import addToHeap, getMaxElement, heapify
def createDandogram(original_graph):

    #dandogram
    G = original_graph.to_undirected()
    partition = community_louvain.best_partition(G)

    # Create a list of nodes and community IDs, converting the node names to numerical IDs
    node_to_id = {node: i for i, node in enumerate(G.nodes())}
    # node_community = [[node_to_id[node], community_id] for node, community_id in partition.items()]

    # Generate the dendrogram
    dendrogram_list = community_louvain.generate_dendrogram(G, part_init=partition)

    # Get the communities for all levels
    for level in range(len(dendrogram_list)):
        partition = community_louvain.partition_at_level(dendrogram_list, level)
        communities = {}
        for node, community_id in partition.items():
            if community_id not in communities:
                communities[community_id] = []
            communities[community_id].append(node)
        print(f"Level {level}: {communities}")

    return communities


def executeSCD(G,communities, k_param, implementation_param):
    # Get the communities for all levels
    heap = []
    for community_id in communities:
        num_of_spammers = 0
        for node in communities[community_id]:
            if(G.nodes[node]['color']=='red'):
                num_of_spammers+=1
        print(f"community {community_id} spamminess is: { num_of_spammers/len(communities[community_id])}")
        addToHeap(heap,community_id, num_of_spammers/len(communities[community_id]))

    communitiesUnion = []
    heapify(heap)
    while(len(communitiesUnion)<k_param*implementation_param):
        maxElement = getMaxElement(heap)
        community_id = maxElement[1]
        print("community_id: ",community_id)
        print("communities[community_id]: ",communities[community_id])
        communitiesUnion = communitiesUnion + communities[community_id]
        print("communitiesUnion: ", communitiesUnion)

    return communitiesUnion