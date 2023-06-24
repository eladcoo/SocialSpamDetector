import matplotlib.pyplot as plt
import networkx as nx

from BE.rawDataExtractor import extract_from_dir, enrich_graph_with_content


# def getStats(G):
#     print("Before: Number of nodes: ")
#     print(G.number_of_nodes())
#     red_nodes = 0
#     for node in G.nodes():
#         if G.nodes[node]['color'] == 'red':
#             red_nodes += 1
#     print("After - Number of spam nodes:", red_nodes)
#
#     blue_nodes = 0
#     for node in G.nodes():
#         if G.nodes[node]['color'] == 'blue':
#             blue_nodes += 1
#
#     print("After - Number of ham nodes:", blue_nodes)
#
# def buildTrainingGraph(hamPath, spamPath):
#     G = nx.DiGraph()
#     print("the nodes in G: ", G.nodes())
#     hamContent = extractFromDir(hamPath)
#     enrichGraphWithContent(G,hamContent)
#     print("the nodes in G after enrichment: ", G.nodes())
#     spamContent = extractFromDir(spamPath)
#     enrichGraphWithContent(G,spamContent,"spam")
#
#     #Draw the graph
#
#     pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
#     # nodes
#     nx.draw_networkx_nodes(G, pos, node_size=700)
#
#     # edges
#     nx.draw_networkx_edges(G, pos, edgelist=G.edges(data=True), width=6)
#
#     # node labels
#     nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
#     # edge weight labels
#     edge_labels = nx.get_edge_attributes(G, "weight")
#     nx.draw_networkx_edge_labels(G, pos, edge_labels)
#
#     for node in G.nodes():
#         if('color' not in G.nodes[node]):
#             G.nodes[node]['color'] = 'blue'
#
#     # node_colors = [G.nodes[node]['color'] for node in G.nodes()]
#     # nx.draw(G, pos, node_color=node_colors)
#     #
#     #
#     #
#     #
#     # ax = plt.gca()
#     # ax.margins(0.08)
#     # plt.axis("off")
#     # plt.tight_layout()
#     # plt.show()
#
#     #Execute undersampaling to equal the number of spammers and legitimate accounts
#     getStats(G)
#     executeUndersampaling(G,True)
#     executeUndersampaling(G,False)
#     getStats(G)
#
#     return G


def build_communication_graph(path):
    G = nx.DiGraph()
    content = extract_from_dir(path)
    enrich_graph_with_content(G, content)

    return G