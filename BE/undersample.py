def executeUndersampaling(G, is_spam):
    # Get the communities for all levels
    desired_color = 'red' if is_spam else 'blue'
    num_of_desired_nodes = 0
    nodes_to_delete = []
    for node in G.nodes:
        if(G.nodes[node]['color']==desired_color):
            num_of_desired_nodes+=1
            if(num_of_desired_nodes>720):
                nodes_to_delete.append(node)
    for node in nodes_to_delete:
        G.remove_node(node)

    return G