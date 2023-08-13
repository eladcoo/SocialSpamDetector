import threading

from BE.accountLevelDetector import execute_ALD
from BE.communicationGraph import build, draw
from BE.spammerCommunitiesDetector import create_communities, execute_SCD

def run_algorithm(path, num_of_rotations, implementation_param, k_param,should_export_graph):

    #Create commmunication graph
    communication_graph = build(path)

    if should_export_graph:
        print("drawing graph")
        # draw_graph(communication_graph)
        graph_thread = threading.Thread(target=draw, args=(communication_graph,))
        graph_thread.start()

    communities = create_communities(communication_graph)
    top_suspect_communities = execute_SCD(communication_graph, communities, k_param, implementation_param)
    print("scd result:", top_suspect_communities)

    suspect_list = execute_ALD(top_suspect_communities,communities,communication_graph,num_of_rotations, k_param)
    return suspect_list



# run_algorithm('../resources/dataToTest',5,5,5,5)