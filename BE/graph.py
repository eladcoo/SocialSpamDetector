import matplotlib.pyplot as plt
import networkx as nx

from BE.rawDataExtractor import extract_from_dir, enrich_graph_with_content

def draw_graph(G):
    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(data=True), width=6)

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    nx.draw(G, pos, node_color=node_colors)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def build_communication_graph(path):
    G = nx.DiGraph()
    content = extract_from_dir(path)
    enrich_graph_with_content(G, content)

    return G