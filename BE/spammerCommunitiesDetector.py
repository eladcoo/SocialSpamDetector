import community as community_louvain

from BE.communityManager import add_account_to_heap, get_max_element, heapify


def create_communities(original_graph):
    G = original_graph.to_undirected()

    # Generate the dendrogram
    dendrogram_list = community_louvain.generate_dendrogram(G)
    communities = {}
    # Get the communities for all levels
    for level in range(len(dendrogram_list)):
        partition = community_louvain.partition_at_level(dendrogram_list, level)
        communities[level] = {}
        for node, community_id in partition.items():
            if community_id not in communities[level]:
                communities[level][community_id] = []
            communities[level][community_id].append(node)
        # print(f"Level {level}: {communities[level].keys()}")

    return communities


def execute_SCD(G, communities, k_param, implementation_param):
    # Get the communities for all levels
    heap = []
    for level in communities:
        for community_id in communities[level]:
            community = communities[level][community_id]
            num_of_spammers = 0
            for node in community:
                if(G.nodes[node]['color']=='red'):
                    num_of_spammers+=1
            # print(f"community {community_id} spamminess is: { num_of_spammers/len(community)}")
            add_account_to_heap(heap, f"{level}-{community_id}", num_of_spammers / len(community))

    top_suspect_communities = []
    suspect_set = []
    heapify(heap)
    while((len(suspect_set)<k_param*implementation_param) and heap):
        maxElement = get_max_element(heap)
        community = maxElement[1]
        level = int(community.split('-')[0])
        community_id = int(community.split('-')[1])
        top_suspect_communities.append(community)
        for account in communities[level][community_id]:
            if (G.nodes[account]['color'] == 'blue'):
                suspect_set.append(account)

    return top_suspect_communities
