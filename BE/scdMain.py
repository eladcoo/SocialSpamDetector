from sklearn.feature_extraction import DictVectorizer

from BE.RotatingForestAlg import train_model
from BE.accountLevelDetector import extract_global_features, extract_local_features
from BE.communityManager import add_account_to_heap, get_max_element, heapify
from BE.graph import build_communication_graph, draw_graph
from BE.spammerCommunitiesDetector import create_communities, execute_SCD

def run_algorithm(path, num_of_rotations, implementation_param, k_param,should_export_graph):

    print("IM HERE!")

    #Create commmunication graph
    communication_graph = build_communication_graph(path)
    communities = create_communities(communication_graph)
    top_suspect_communities = execute_SCD(communication_graph, communities, k_param, implementation_param)

    print("scd result:", top_suspect_communities)

    #train model
    global_features = extract_global_features(communication_graph)
    local_features = extract_local_features(communication_graph,communities)

    rf_models = train_model(communication_graph, communities, global_features, local_features, num_of_rotations)

    heap = []
    vec = DictVectorizer()

    #  for each community and for each account in that community - run ML on that account and insert the score to a max heap
    for community in top_suspect_communities:
        level = int(community.split('-')[0])
        community_id = int(community.split('-')[1])
        for account in communities[level][community_id]:
            account_feature = {}
            account_feature.update(global_features[account])
            account_feature.update(local_features[account][community])
            account_feature_data = vec.fit_transform(account_feature).toarray()
            score = rf_models[level].predict(account_feature_data)
            print("score:", score[0])
            add_account_to_heap(heap,account,score[0])

    heapify(heap)
    #show the K most suspicious accounts
    suspect_list = []
    while len(suspect_list) < k_param:
        account = get_max_element(heap)
        if account not in suspect_list:
            suspect_list.append(account)

    print("suspect_list: ", suspect_list)

    if should_export_graph:
        draw_graph(communication_graph)

    return suspect_list

# run_algorithm('../resources/dataToTest',5,5,5,5)