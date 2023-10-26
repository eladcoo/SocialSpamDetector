import matplotlib.pyplot as plt
import networkx as nx

from BE.rawDataExtractor import extract_from_dir

def draw(G):
    pos = nx.random_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=10)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(data=True), width=1)

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=5, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=5)

    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    nx.draw(G, pos, node_color=node_colors)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.ioff()
    plt.show()

    print("Done drawing the graph!")

# Since the spam is tagged on the edge, we need to check all th edge of the node
def is_a_spammer_node(dest_nodes):
    is_spam = False
    for dest_node in dest_nodes:
        is_spam = is_spam or dest_node['is_spam']
    return is_spam

# Build graph with tags and weights
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
def build(path):
    G = nx.DiGraph()
    content = extract_from_dir(path)
    enrich_graph_with_content(G, content)

    return G